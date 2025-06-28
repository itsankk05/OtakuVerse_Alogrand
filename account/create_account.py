from algosdk import account, mnemonic
from utils.algod_client import get_algod_client
algod_client = get_algod_client()
# Create a new account
private_key, address = account.generate_account()

# Generate mnemonic (25-word recovery phrase)
mnemonic_phrase = mnemonic.from_private_key(private_key)

# print("🎉 New Algorand Account Created:")
# print(f"address: {address}")
# print(f"private key: {private_key}")
# print(f"mnemonic: {mnemonic.from_private_key(private_key)}")

account_info: Dict[str, Any] = algod_client.account_info(address)
print(f"Account balance: {account_info.get('amount')} microAlgos")