import json
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from enum import Enum
from logging import Logger
from pathlib import Path
from typing import Any, Callable, Final

import pandas as pd
import requests
from eth_abi import encode
from eth_account import Account
from ratelimit import limits, sleep_and_retry
from requests import Response
from tenacity import retry, stop_after_attempt, wait_exponential
from web3 import Web3
from web3.contract import Contract
from web3.types import ChecksumAddress

from pyrfx.config_manager import ConfigManager

PRECISION: Final[int] = 30

# Set up logging
logging.basicConfig(level=logging.INFO)
logger: Logger = logging.getLogger(__name__)


# Enum for Order Types
class OrderTypes(Enum):
    MARKET_SWAP = 0
    LIMIT_SWAP = 1
    MARKET_INCREASE = 2
    LIMIT_INCREASE = 3
    MARKET_DECREASE = 4
    LIMIT_DECREASE = 5
    STOP_LOSS_DECREASE = 6
    LIQUIDATION = 7


# Enum for Decrease Position Swap Types
class DecreasePositionSwapTypes(Enum):
    NO_SWAP = 0
    SWAP_PNL_TOKEN_TO_COLLATERAL_TOKEN = 1
    SWAP_COLLATERAL_TOKEN_TO_PNL_TOKEN = 2


# Constants for rate limiting
CALLS_PER_SECOND: Final[int] = 5
ONE_SECOND: Final[int] = 1


# Rate limiter decorator (allows 5 calls per second)
@sleep_and_retry
@limits(calls=CALLS_PER_SECOND, period=ONE_SECOND)
def rate_limited_call(call) -> Any:
    """
    Wrapper to rate-limit Web3 calls.
    """
    return call.call()


# Retrier decorator (exponential backoff with a maximum of 3 retries)
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def execute_call(call) -> Any:
    """
    Executes a Web3 call with retry logic and rate limiting.

    :param call: Web3 call to be executed.
    :return: The result of the Web3 call.
    """
    try:
        result = rate_limited_call(call)
        logger.debug("Web3 call executed successfully.")
        return result
    except Exception as e:
        logger.error(f"Error during Web3 call execution: {e}")
        raise


# Executes multiple Web3 calls concurrently using ThreadPoolExecutor
def execute_threading(function_calls: list) -> list:
    """
    Execute multiple Web3 function calls concurrently using ThreadPoolExecutor.

    :param function_calls: A list of Web3 function calls to execute.
    :return: A list of results from the executed Web3 calls.
    """
    logger.info("Starting multithreaded Web3 calls.")
    try:
        with ThreadPoolExecutor() as executor:
            results: list = list(executor.map(execute_call, function_calls))
        logger.info("All Web3 calls executed successfully.")
        return results
    except Exception as e:
        logger.error(f"Error during multithreaded Web3 execution: {e}")
        raise


# Gets the parent folder of the current script
def _get_parent_folder() -> Path:
    """
    Private method to get the parent folder of the current script.

    :return: Path of the parent folder of the current script.
    """
    return Path(__file__).parent


# Helper function to load ABI
def _load_contract_abi(abi_file_path: Path) -> list[dict[str, Any]]:
    """
    Load the ABI file from the specified path.

    :param abi_file_path: Path to the ABI JSON file.
    :return: Loaded ABI as a list of dictionaries.
    :raises FileNotFoundError: If the file doesn't exist.
    :raises json.JSONDecodeError: If the JSON content is invalid.
    """
    try:
        with abi_file_path.open("r", encoding="utf-8") as abi_file:
            return json.load(abi_file)
    except FileNotFoundError as e:
        logger.error(f"ABI file not found: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding ABI file {abi_file_path}: {e}")
        raise


# General function to get contract object
def get_contract_object(config: ConfigManager, contract_name: str) -> Contract:
    """
    Retrieve and instantiate a Web3 contract object using the contract name and chain.

    :param config: Configuration manager containing blockchain settings.
    :param contract_name: Name of the contract.
    :return: A Web3 contract object.
    :raises ValueError: If the contract information or ABI file is missing or invalid.
    :raises FileNotFoundError: If the ABI file is not found.
    :raises json.JSONDecodeError: If the ABI file is not valid JSON.
    """
    try:
        # Build the path to the ABI file using Path
        abi_file_path: Path = _get_parent_folder() / config.contracts[contract_name].abi_path
        logger.info(f"Loading ABI file from {abi_file_path}")

        # Load contract ABI
        contract_abi: list[dict[str, Any]] = _load_contract_abi(abi_file_path)

        # Return the Web3 contract object
        contract: Contract = config.connection.eth.contract(
            address=config.contracts[contract_name].contract_address, abi=contract_abi
        )
        logger.info(f"Contract object for '{contract_name}' on chain '{config.chain}' created successfully.")
        return contract

    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading ABI for contract {contract_name}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while creating contract object: {e}")
        raise


# Retrieve token balance contract
def get_token_balance_contract(config: ConfigManager, contract_address: str) -> Contract | None:
    """
    Retrieve the contract object required to query a user's token balance.

    :param config: Configuration object containing RPC and chain details.
    :param contract_address: The token contract address to query balance from.
    :return: Web3 contract object or None if an error occurs.
    """
    try:
        # Build the path to the ABI file using Path
        abi_file_path: Path = _get_parent_folder() / "contracts" / "balance_abi.json"

        # Load contract ABI
        contract_abi = _load_contract_abi(abi_file_path)

        # Convert the contract address to ChecksumAddress
        contract_address: ChecksumAddress = config.to_checksum_address(address=contract_address)

        # Return the instantiated contract object
        contract = config.connection.eth.contract(address=contract_address, abi=contract_abi)
        logger.debug(f"Contract for token balance at address {contract_address} successfully created.")
        return contract

    except Exception as e:
        logger.error(f"Error creating token balance contract: {e}")
        return None


# Fetch available tokens
def get_available_tokens(config: ConfigManager) -> dict[str, dict[str, str | int | bool]]:
    """
    Query the RFX API to generate a dictionary of available tokens for the specified chain.

    :param config: Configuration object containing the chain information.
    :return: Dictionary of available tokens.
    """
    try:
        response: Response = requests.get(config.tokens_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        token_infos: list[dict[str, str | int]] = response.json().get("tokens", [])
        logger.info(f"Successfully fetched available tokens for chain {config.chain}.")
    except requests.RequestException as e:
        logger.error(f"Error fetching tokens from API for chain {config.chain}: {e}")
        raise requests.RequestException(f"Error fetching tokens from API for chain {config.chain}: {e}")

    return {token_info["address"]: token_info for token_info in token_infos}


# Retrieve reader contract
def get_synthetics_reader_contract(config: ConfigManager) -> Contract:
    """
    Retrieve the reader contract object for the specified chain.

    :param config: Configuration object.
    :return: Reader contract object.
    """
    return get_contract_object(config=config, contract_name="synthetics_reader")


# Retrieve event emitter contract
def get_event_emitter_contract(config: ConfigManager) -> Contract:
    """
    Get an event emitter contract for a given chain.

    :param config: Configuration object containing the chain information.
    :return: Web3 contract object for event emitter.
    """
    return get_contract_object(config=config, contract_name="event_emitter")


# Retrieve datastore contract
def get_data_store_contract(config: ConfigManager) -> Contract:
    """
    Get a datastore contract for a given chain.

    :param config: Configuration object containing the chain information.
    :return: Web3 contract object for datastore.
    """
    return get_contract_object(config=config, contract_name="data_store")


# Retrieve exchange router contract
def get_exchange_router_contract(config: ConfigManager) -> Contract:
    """
    Get an exchange router contract for a given chain.

    :param config: Configuration object containing the chain information.
    :return: Web3 contract object for exchange router.
    """
    return get_contract_object(config=config, contract_name="exchange_router")


def create_signer(config: ConfigManager) -> Account | None:
    """
    Create a signer for the given chain using the private key.

    :param config: Configuration object containing the private key and chain information.
    :return: Web3 account object initialized with the private key or None if an error occurs.
    """
    try:
        account = config.connection.eth.account.from_key(config.private_key)
        logger.info("Signer account created successfully.")
        return account
    except Exception as e:
        logger.error(f"Error creating signer: {e}")
        return None


def create_hash(data_type_list: list[str], data_value_list: list) -> bytes:
    """
    Create a keccak hash using a list of data types and their corresponding values.

    :param data_type_list: List of data types as strings.
    :param data_value_list: List of values corresponding to the data types.
    :return: Encoded and hashed key in bytes.
    """
    try:
        byte_data: bytes = encode(data_type_list, data_value_list)
        hash_result = Web3.keccak(byte_data)
        logger.debug("Keccak hash created successfully.")
        return hash_result
    except Exception as e:
        logger.error(f"Error creating hash: {e}")
        raise


def create_hash_string(string: str) -> bytes:
    """
    Create a keccak hash for a given string.

    :param string: The string to hash.
    :return: Hashed string in bytes.
    """
    try:
        hash_result = create_hash(["string"], [string])
        logger.debug("Keccak hash for string created successfully.")
        return hash_result
    except Exception as e:
        logger.error(f"Error creating hash for string: {e}")
        raise


def get_execution_price_and_price_impact(
    config: ConfigManager, params: dict[str, Any], decimals: int
) -> dict[str, float]:
    """
    Get the execution price and price impact for a position.

    :param config: Configuration object.
    :param params: Dictionary of the position parameters.
    :param decimals: Number of decimals for the token being traded.
    :return: A dictionary containing the execution price and price impact.
    """
    reader_contract: Contract = get_synthetics_reader_contract(config)

    output = execute_contract_function(
        reader_contract.functions.getExecutionPrice,
        params["data_store_address"],
        params["market_key"],
        params["index_token_price"],
        params["position_size_in_usd"],
        params["position_size_in_tokens"],
        params["size_delta"],
        params["is_long"],
    )

    if output:
        return {
            "execution_price": output[2] / 10 ** (30 - decimals),
            "price_impact_usd": output[0] / 10**30,
        }
    else:
        logger.error("Failed to get execution price and price impact.")
        return {"execution_price": 0.0, "price_impact_usd": 0.0}


def execute_contract_function(contract_function: Callable[..., Any], *args: Any) -> Any | None:
    """
    Execute a contract function call and return the result or handle exceptions.

    :param contract_function: The contract function to call.
    :param args: Arguments to pass to the contract function.
    :return: The result of the contract function call or None if an error occurs.
    """
    try:
        return contract_function(*args).call()
    except Exception as e:
        logger.error(f"Error executing contract function '{str(contract_function)}' with arguments {args}: {e}")
        return None


def get_estimated_swap_output(config: ConfigManager, params: dict[str, Any]) -> dict[str, float]:
    """
    Get the estimated swap output amount and price impact for a given chain and swap parameters.

    :param config: Configuration object containing chain information.
    :param params: Dictionary of the swap parameters.
    :return: A dictionary with the estimated token output and price impact.
    """
    reader_contract: Contract = get_synthetics_reader_contract(config)
    output: tuple[int, int] = execute_contract_function(
        reader_contract.functions.getSwapAmountOut,
        params["data_store_address"],
        params["market_addresses"],
        params["token_prices_tuple"],
        params["token_in"],
        params["token_amount_in"],
        params["ui_fee_receiver"],
    )

    if output:
        return {
            "out_token_amount": output[0],
            "price_impact_usd": output[1],
        }
    else:
        logger.error("Failed to get swap output.")
        return {"out_token_amount": 0.0, "price_impact_usd": 0.0}


def get_estimated_deposit_amount_out(config: ConfigManager, params: dict[str, Any]) -> Any | None:
    """
    Get the estimated deposit amount output for a given chain and deposit parameters.

    :param config: Configuration object containing chain information.
    :param params: Dictionary of the deposit parameters.
    :return: The output of the deposit amount calculation or None if an error occurs.
    """
    reader_contract = get_synthetics_reader_contract(config)
    return execute_contract_function(
        reader_contract.functions.getDepositAmountOut,
        params["data_store_address"],
        params["market_addresses"],
        params["token_prices_tuple"],
        params["long_token_amount"],
        params["short_token_amount"],
        params["ui_fee_receiver"],
    )


def get_estimated_withdrawal_amount_out(config: ConfigManager, params: dict[str, Any]) -> Any | None:
    """
    Get the estimated withdrawal amount output for a given chain and withdrawal parameters.

    :param config: Configuration object containing chain information.
    :param params: Dictionary of the withdrawal parameters.
    :return: The output of the withdrawal amount calculation or None if an error occurs.
    """
    reader_contract = get_synthetics_reader_contract(config)
    return execute_contract_function(
        reader_contract.functions.getWithdrawalAmountOut,
        params["data_store_address"],
        params["market_addresses"],
        params["token_prices_tuple"],
        params["gm_amount"],
        params["ui_fee_receiver"],
    )


def find_dictionary_by_key_value(outer_dict: dict[str, Any], key: str, value: str) -> dict[str, Any] | None:
    """
    Search for a dictionary by key-value pair within an outer dictionary.

    :param outer_dict: The outer dictionary to search.
    :param key: The key to search for.
    :param value: The value to match.
    :return: The dictionary containing the matching key-value pair, or None if not found.
    """
    for inner_dict in outer_dict.values():
        if key in inner_dict and inner_dict[key] == value:
            return inner_dict
    return None


def apply_factor(value: int, factor: int) -> int:
    """
    Apply a factor to a value.

    :param value: The base value.
    :param factor: The factor to apply.
    :return: The adjusted value.
    """
    return value * factor // 10**30


def get_funding_factor_per_period(
    market_info: dict, is_long: bool, period_in_seconds: int, long_interest_usd: int, short_interest_usd: int
) -> float:
    """
    Calculate the funding factor for a given period in a market.

    :param market_info: Dictionary of market parameters returned from the reader contract.
    :param is_long: Boolean indicating the direction of the position (long or short).
    :param period_in_seconds: The period in seconds over which to calculate the funding factor.
    :param long_interest_usd: Long interest in expanded decimals.
    :param short_interest_usd: Short interest in expanded decimals.
    :return: The funding factor for the specified period.
    """
    try:
        funding_factor_per_second = market_info["funding_factor_per_second"] * 10**-28
        long_pays_shorts = market_info["is_long_pays_short"]

        if is_long:
            is_larger_side = long_pays_shorts
        else:
            is_larger_side = not long_pays_shorts

        if is_larger_side:
            return funding_factor_per_second * -1 * period_in_seconds

        larger_interest_usd = long_interest_usd if long_pays_shorts else short_interest_usd
        smaller_interest_usd = short_interest_usd if long_pays_shorts else long_interest_usd

        ratio = larger_interest_usd * 10**30 / smaller_interest_usd if smaller_interest_usd > 0 else 0
        return apply_factor(ratio, funding_factor_per_second) * period_in_seconds

    except KeyError as e:
        logging.error(f"Key error in market information: {e}")
        return 0.0


def save_json_file_to_datastore(filename: str, data: dict) -> None:
    """
    Save a dictionary as a JSON file in the datastore directory.

    :param filename: Name of the JSON file.
    :param data: Dictionary data to save.
    """
    try:
        filepath: Path = _get_parent_folder() / "data_store" / filename
        with filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"Data saved to: {filepath}")
    except Exception as e:
        logging.error(f"Error saving data to {filename}: {e}")


def make_timestamped_dataframe(data: dict) -> pd.DataFrame:
    """
    Convert a dictionary into a Pandas DataFrame with a timestamp column.

    :param data: Dictionary data to convert.
    :return: DataFrame with timestamp column added.
    """
    dataframe = pd.DataFrame([data])  # Create DataFrame from single row of data
    dataframe["timestamp"] = datetime.now()
    return dataframe


def save_csv_to_datastore(filename: str, dataframe: pd.DataFrame) -> None:
    """
    Save a Pandas DataFrame as a CSV file in the datastore.

    :param filename: Name of the CSV file.
    :param dataframe: Pandas DataFrame to save.
    """
    try:
        filepath: Path = _get_parent_folder() / "data_store" / filename

        # Append to existing file if it exists
        if filepath.exists():
            existing_data = pd.read_csv(filepath)
            dataframe = pd.concat([existing_data, dataframe], ignore_index=True)

        dataframe.to_csv(filepath, index=False)
        logging.info(f"Dataframe saved to {filepath}")
    except Exception as e:
        logging.error(f"Error saving dataframe to {filename}: {e}")


def determine_swap_route(config: ConfigManager, markets: dict, in_token: str, out_token: str) -> tuple[list[str], bool]:
    """
    Find the list of RFX markets required to swap from one token to another.

    :param config: ConfigManager object containing chain configuration.
    :param markets: Dictionary of available markets.
    :param in_token: Contract address of the input token.
    :param out_token: Contract address of the output token.
    :return: A tuple containing the list of RFX markets and a boolean indicating if multi-swap is required.
    """
    try:
        # If USDC->token, search for token->USDC
        if in_token == config.usdc_address:
            rfx_market_address: str | None = find_dictionary_by_key_value(
                outer_dict=markets, key="index_token_address", value=out_token
            ).get("rfx_market_address")
        else:
            # TODO: Fix the case if in_token == WBTC.e, then in_token = BTC2 address
            rfx_market_address: str | None = find_dictionary_by_key_value(
                outer_dict=markets, key="index_token_address", value=in_token
            ).get("rfx_market_address")

        if not rfx_market_address:
            raise ValueError(f"No market found for out_token: {out_token}")

        if out_token != config.usdc_address and in_token != config.usdc_address:
            # TODO: Make this more generic and use more than 2 swaps. E.g. for swap from A->D, find A->B->C->D
            second_rfx_market_address: str | None = find_dictionary_by_key_value(
                markets, "index_token_address", out_token
            ).get("rfx_market_address")

            # (swap_path, is_requires_multi_swap)
            return [rfx_market_address, second_rfx_market_address], True

        # (swap_path, is_requires_multi_swap)
        return [rfx_market_address], False

    except Exception as e:
        logging.error(f"Error determining swap route: {e}")
        return [], False
