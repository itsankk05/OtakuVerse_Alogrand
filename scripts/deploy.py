import os
from dotenv import load_dotenv
from algosdk import account, mnemonic, encoding
from algosdk.v2client import algod
from algosdk.transaction import (
    ApplicationCreateTxn,
    OnComplete,
    StateSchema,
)
from pyteal import compileTeal, Mode
import base64
from utils.algod_client import get_algod_client
from contracts.nft_data_contract import nft_data_approval, nft_data_clear
from contracts.mint_nft import approval_program, clear_state_program
import time
import json
from uuid import uuid4

load_dotenv()
algod_client = get_algod_client()

creator_mnemonic = os.getenv("CREATOR_MNEMONIC")
creator_private_key = mnemonic.to_private_key(creator_mnemonic)
creator_address = account.address_from_private_key(creator_private_key)


def deploy_teal_contract(
    approval_teal_src: str,
    clear_teal_src: str,
    global_schema: StateSchema,
    local_schema: StateSchema = StateSchema(0, 0),
    app_args: list = None,
    sender: str = None,
):
    """Compiles TEAL source and returns a base64-encoded unsigned transaction."""
    approval_result = algod_client.compile(approval_teal_src)["result"]
    clear_result = algod_client.compile(clear_teal_src)["result"]

    note = json.dumps({"uid": str(uuid4())}).encode()

    txn = ApplicationCreateTxn(
        sender=sender or creator_address,
        sp=algod_client.suggested_params(),
        on_complete=OnComplete.NoOpOC,
        approval_program=base64.b64decode(approval_result),
        clear_program=base64.b64decode(clear_result),
        global_schema=global_schema,
        local_schema=local_schema,
        app_args=app_args or [],
        note=note,
    )

    # ✅ Encode transaction in base64 using msgpack
    txn_b64 = encoding.msgpack_encode(txn)
    tx_id = txn.get_txid()

    return {
        "success": True,
        "txn": txn_b64,
        "tx_id": tx_id,  # return to frontend so it can be confirmed later
    }


def deploy_mint_nft_contract():
    approval_src = compileTeal(approval_program(), mode=Mode.Application, version=6)
    clear_src = compileTeal(clear_state_program(), mode=Mode.Application, version=6)

    return deploy_teal_contract(
        approval_teal_src=approval_src,
        clear_teal_src=clear_src,
        global_schema=StateSchema(0, 0),
    )


def deploy_nft_data_contract(metadata_cid: str, image_cid: str, wallet_address: str):
    approval_src = compileTeal(nft_data_approval(), mode=Mode.Application, version=6)
    clear_src = compileTeal(nft_data_clear(), mode=Mode.Application, version=6)

    return deploy_teal_contract(
        approval_teal_src=approval_src,
        clear_teal_src=clear_src,
        global_schema=StateSchema(num_uints=0, num_byte_slices=3),
        app_args=[metadata_cid.encode(), image_cid.encode()],
        sender=wallet_address,
    )
