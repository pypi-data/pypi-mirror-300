import logging

from web3.contract import Contract
from web3.contract.contract import ContractFunction

from pyrfx.config_manager import ConfigManager
from pyrfx.keys import (
    decrease_order_gas_limit_key,
    deposit_gas_limit_key,
    execution_gas_fee_base_amount_key,
    execution_gas_fee_multiplier_key,
    increase_order_gas_limit_key,
    single_swap_gas_limit_key,
    swap_order_gas_limit_key,
    withdraw_gas_limit_key,
)
from pyrfx.utils import apply_factor, get_data_store_contract


def get_execution_fee(
    gas_limits: dict[str, ContractFunction], estimated_gas_limit_contract_function: ContractFunction, gas_price: int
) -> int:
    """
    Calculate the minimum execution fee required to perform an action based on gas limits and gas price.

    :param gas_limits: A dictionary of uncalled datastore limit functions.
    :param estimated_gas_limit_contract_function: The uncalled datastore contract function specific to the operation
        being undertaken.
    :param gas_price: The current gas price.
    :return: The adjusted gas fee to cover the execution cost.
    """
    base_gas_limit: int = gas_limits["estimated_fee_base_gas_limit"].call()
    multiplier_factor: int = gas_limits["estimated_fee_multiplier_factor"].call()
    estimated_gas: int = estimated_gas_limit_contract_function.call()

    adjusted_gas_limit: int = base_gas_limit + apply_factor(estimated_gas, multiplier_factor)

    return int(adjusted_gas_limit * gas_price)


def get_gas_limits(datastore_object: Contract) -> dict[str, ContractFunction]:
    """
    Retrieve gas limit functions from the datastore contract for various operations requiring execution fees.

    :param datastore_object: A Web3 contract object for accessing the datastore.
    :return: A dictionary of uncalled gas limit functions corresponding to various operations.
    """
    gas_limits: dict[str, ContractFunction] = {
        "deposit": datastore_object.functions.getUint(deposit_gas_limit_key()),
        "withdraw": datastore_object.functions.getUint(withdraw_gas_limit_key()),
        "single_swap": datastore_object.functions.getUint(single_swap_gas_limit_key()),
        "swap_order": datastore_object.functions.getUint(swap_order_gas_limit_key()),
        "increase_order": datastore_object.functions.getUint(increase_order_gas_limit_key()),
        "decrease_order": datastore_object.functions.getUint(decrease_order_gas_limit_key()),
        "estimated_fee_base_gas_limit": datastore_object.functions.getUint(execution_gas_fee_base_amount_key()),
        "estimated_fee_multiplier_factor": datastore_object.functions.getUint(execution_gas_fee_multiplier_key()),
    }

    return gas_limits


if __name__ == "__main__":
    # Initialise logging
    from pyrfx.logging_setup import logging_setup

    logging_setup()

    # Initialize config
    config: ConfigManager = ConfigManager(chain="arbitrum")
    logging.info(config)

    # Get the contract object for the datastore
    datastore_object: Contract = get_data_store_contract(config=config)

    # Retrieve gas limits
    gas_limits: dict[str, ContractFunction] = get_gas_limits(datastore_object)

    # Get the current gas price from the network
    gas_price: int = config.connection.eth.gas_price

    # Calculate the execution fee for increasing an order
    execution_fee: int = get_execution_fee(gas_limits, gas_limits["increase_order"], gas_price)

    logging.info(f"Execution fee for increasing order: {execution_fee}")
