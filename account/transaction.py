import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.algod_client import get_algod_client
from dotenv import load_dotenv
from algosdk import transaction
import json
from base64 import b64decode

load_dotenv()
address = os.getenv("ALGORAND_ADDRESS")
address2 = os.getenv("ALGORAND_ADDRESS_2")
private_key = os.getenv("PRIVATE_KEY")


algod_client = get_algod_client()
params = algod_client.suggested_params()
unsigned_txn = transaction.PaymentTxn(
    sender=address,
    sp=params,
    receiver=address2,
    amt=1000000,
    note=b"Hello World",
)

signed_txn = unsigned_txn.sign(private_key)

txid = algod_client.send_transaction(signed_txn)
print("Successfully submitted transaction with txID: {}".format(txid))

# wait for confirmation
txn_result = transaction.wait_for_confirmation(algod_client, txid, 4)

print(f"Transaction information: {json.dumps(txn_result, indent=4)}")
print(f"Decoded note: {b64decode(txn_result['txn']['txn']['note'])}")