import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.algod_client import get_algod_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Algod client
algod_client = get_algod_client()

# Get account address from .env
address = os.getenv("ALGORAND_ADDRESS")
address2 = os.getenv("ALGORAND_ADDRESS_2")

# if not address:
#     print("❌ ERROR: Please set MY_ALGORAND_ADDRESS in your .env file")
#     exit(1)

# Fetch account info
try:
    account_info = algod_client.account_info(address)
    account_info2 = algod_client.account_info(address2)
    balance = account_info.get("amount", 0)
    balance2 = account_info2.get("amount", 0)
    print(f"📬 Address: {address}")
    print(f"💰 Balance: {balance} microAlgos ({balance / 1_000_000:.6f} Algos)")
    print(f"📬 Address 2: {address2}")
    print(f"💰 Balance 2: {balance2} microAlgos ({balance2 / 1_000_000:.6f} Algos)")
except Exception as e:
    print(f"❌ Failed to retrieve balance: {e}")
