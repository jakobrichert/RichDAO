

from algosdk import  mnemonic
from algosdk.constants import microalgos_to_algos_ratio, min_txn_fee
from algosdk.error import  WrongMnemonicLengthError
from algosdk.future.transaction import AssetConfigTxn
from algosdk.v2client import algod


INITIAL_FUNDS = 1000000000  # in microAlgos











## CLIENTS
def _algod_client():
    """Instantiate and return Algod client object."""
    algod_address = "youre algo address"
    algod_token = "your algod token"
    return algod.AlgodClient(algod_token, algod_address)





## TRANSACTIONS
def _wait_for_confirmation(client, transaction_id, timeout):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """
    start_round = client.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:
            raise Exception("pool error: {}".format(pending_txn["pool-error"]))
        client.status_after_block(current_round)
        current_round += 1
    raise Exception(
        "pending tx not found in timeout rounds, timeout value = : {}".format(timeout)
    )




## CREATING
def add_asset(data):
    """Create asset from provided data dictionary."""
    client = _algod_client()
    params = client.suggested_params()
    unsigned_txn = AssetConfigTxn(
        sp=params,
        sender=data.get("creator"),
        asset_name=data.get("name"),
        unit_name=data.get("unit"),
        total=data.get("total"),
        decimals=data.get("decimals"),
        default_frozen=data.get("frozen"),
        url=data.get("url"),
        manager=data.get("manager"),
        reserve=data.get("reserve"),
        freeze=data.get("freeze"),
        clawback=data.get("clawback"),
        
        strict_empty_address_check=False,
    )
    # Sign with secret key of creator
    try:
        signed_txn = unsigned_txn.sign(mnemonic.to_private_key(data.get("passphrase")))
    except WrongMnemonicLengthError as err:
        return None, err

    try:
        transaction_id = client.send_transaction(signed_txn)
        _wait_for_confirmation(client, transaction_id, 4)
    except Exception as err:
        return None, err





