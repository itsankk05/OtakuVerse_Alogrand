import os
from dotenv import load_dotenv
from algosdk.v2client import algod

load_dotenv()

def get_algod_client():
    algod_address = os.getenv("ALGOD_ADDRESS")
    algod_token = os.getenv("ALGOD_TOKEN")
    headers = {
        "X-API-Key": algod_token
    } if algod_token and algod_token != "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" else {}

    return algod.AlgodClient(algod_token, algod_address, headers)

