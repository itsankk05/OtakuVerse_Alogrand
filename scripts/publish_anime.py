from utils.ipfs_utils import upload_file_to_ipfs, upload_json_to_ipfs
from scripts.deploy import deploy_nft_data_contract
import base64
import traceback


def publish_anime(data):
    try:
        metadata = data.get("metadata")
        wallet = data.get("wallet")

        if not metadata or not wallet:
            return {"success": False, "error": "Missing metadata or wallet"}

        nft_collection = metadata.get("nftCollection", [])
        if not nft_collection:
            return {"success": False, "error": "NFT collection is empty"}

        for nft in nft_collection:
            if "image" in nft and nft["image"].startswith("data:image"):
                base64_data = nft["image"].split(",", 1)[1]
                file_bytes = base64.b64decode(base64_data)
                cid = upload_file_to_ipfs(file_bytes, filename=f"{nft['name']}.png")
                nft["image"] = f"ipfs://{cid}"

        metadata_cid = upload_json_to_ipfs(metadata)

        first_image = nft_collection[0].get("image", "")
        image_cid = (
            first_image.replace("ipfs://", "")
            if first_image.startswith("ipfs://")
            else ""
        )
        print(f"Metadata CID: {metadata_cid}, Image CID: {image_cid}")

        # deploy_nft_data_contract already returns a base64-encoded transaction
        txn_result = deploy_nft_data_contract(metadata_cid, image_cid, wallet)

        txn_base64 = txn_result["txn"]

        return {
            "success": True,
            "ipfs_cid": metadata_cid,
            "txn": txn_base64,
            "updated_metadata": metadata,
        }

    except Exception as e:
        traceback.print_exc()
        return {"success": False, "error": str(e)}
