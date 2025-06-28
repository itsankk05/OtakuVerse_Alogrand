from flask import Blueprint, request, jsonify
from scripts.mint_nft import mint_nft
from scripts.publish_anime import publish_anime
from utils.db_utils import fetch_all_anime_with_nfts
import os
import sys
from scripts.deploy import deploy_nft_data_contract
from utils.db_utils import store_user_contract_mapping, save_anime_to_db

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

nft_routes = Blueprint("nft_routes", __name__)


@nft_routes.route("/mint-nft", methods=["POST"])
def mint_nft_route():
    try:
        data = request.get_json()
        print(f"Received data for minting NFT: {data}")
        response = mint_nft(data)  # ADD DATA mint_nft(data)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@nft_routes.route("/publish-nft", methods=["POST"])
def publish_nft_route():
    try:
        data = request.get_json()
        response = publish_anime(data)

        if isinstance(response, tuple):  # (dict, status_code)
            return jsonify(response[0]), response[1]
        else:
            return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@nft_routes.route("/anime-list", methods=["POST"])
def get_anime_list():
    try:
        data = fetch_all_anime_with_nfts()
        return jsonify({"success": True, "anime": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@nft_routes.route("/get-nft-create-txn", methods=["POST"])
def get_txn():
    data = request.json
    metadata_cid = data["metadata_cid"]
    image_cid = data["image_cid"]
    wallet = data["wallet"]

    txn_dict = deploy_nft_data_contract(metadata_cid, image_cid, wallet)
    return jsonify({"txn": txn_dict})


@nft_routes.route("/store-app-id", methods=["POST"])
def store_app_id():
    data = request.json
    wallet = data.get("wallet")
    app_id = data.get("app_id")

    if not wallet or not app_id:
        return jsonify({"success": False, "error": "Missing wallet or app_id"}), 400

    try:
        store_user_contract_mapping(wallet, app_id)
        print(f"✅ Stored user contract: {wallet} → App ID {app_id}")
        return jsonify({"success": True, "message": "App ID stored"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@nft_routes.route("/submit-anime", methods=["POST"])
def submit_anime():
    try:
        data = request.get_json()
        print(f"Received data for submitting anime: {data}")

        if not data:
            return jsonify({"success": False, "error": "No JSON payload"}), 400

        anime = data.get("anime")
        ipfs_cid = data.get("ipfs_cid", "unknown")
        creator_wallet = data.get("creatorWallet")
        timestamp = data.get("timestamp")

        if not anime or not creator_wallet:
            return (
                jsonify({"success": False, "error": "Missing anime or creator data"}),
                400,
            )

        # Save to DB
        save_anime_to_db(anime, ipfs_cid, creator_wallet)

        # You can optionally also store creator info (add logic for that)
        return jsonify({"success": True, "message": "Anime stored successfully"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@nft_routes.route("/all-anime", methods=["GET"])
def get_all_anime():
    try:
        # Get query params (with defaults)
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 12))
        offset = (page - 1) * limit

        all_anime = fetch_all_anime_with_nfts()

        # Pagination
        total_items = len(all_anime)
        paginated = all_anime[offset : offset + limit]

        return jsonify(
            {"success": True, "data": paginated, "page": page, "total": total_items}
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
