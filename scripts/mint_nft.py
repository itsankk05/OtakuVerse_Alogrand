from flask import request
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.algod_client import get_algod_client
from algosdk import account, mnemonic, transaction
from dotenv import load_dotenv
from algosdk.transaction import wait_for_confirmation

load_dotenv()
algod_client = get_algod_client()
mnemonic_raw = os.getenv("CREATOR_MNEMONIC")
if not mnemonic_raw:
    raise ValueError("❌ CREATOR_MNEMONIC is missing or not loaded from .env")
creator_private_key = mnemonic.to_private_key(mnemonic_raw)
creator_address = account.address_from_private_key(creator_private_key)


def mint_nft(data):
    try:
        print("📥 Incoming mint_nft payload:", data)

        # Extract relevant values from data
        wallet = data.get("userWallet")
        metadata = data.get("nftMetadata", {})
        asset_name = metadata.get("name", "Untitled NFT")[
            :32
        ]  # Algorand asset name max 32 chars
        image_url = metadata.get("image")
        ipfs_cid = metadata.get("ipfs_metadata", {}).get("cid")

        # Validate required fields
        if not asset_name or not ipfs_cid:
            raise ValueError(
                "Missing required NFT metadata fields: asset_name or ipfs_cid"
            )

        # Construct IPFS asset URL (Algorand URL field)
        ipfs_url = f"ipfs://{ipfs_cid}"

        # Build transaction
        params = algod_client.suggested_params()
        txn = transaction.AssetConfigTxn(
            sender=creator_address,
            sp=params,
            total=1,
            default_frozen=False,
            unit_name="OTAKU",  # customize if needed (max 8 chars)
            asset_name=asset_name,
            manager=creator_address,
            reserve=None,
            freeze=None,
            clawback=None,
            url=image_url,
            decimals=0,
            strict_empty_address_check=False,
        )

        signed_txn = txn.sign(creator_private_key)
        txid = algod_client.send_transaction(signed_txn)
        print(f"✅ Transaction sent with txID: {txid}")

        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        asset_id = confirmed_txn["asset-index"]
        print(f"🎉 NFT Minted! Asset ID: {asset_id}")

        return {
            "success": True,
            "txid": txid,
            "asset_id": asset_id,
            "nft_name": asset_name,
            "image_url": image_url,
            "metadata_cid": ipfs_cid,
        }

    except Exception as e:
        print("💥 mint_nft error:", e)
        return {"success": False, "error": str(e)}
