import requests
import os
from dotenv import load_dotenv

load_dotenv()

PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY")
PINATA_BASE_URL = "https://api.pinata.cloud/pinning/"

def upload_file_to_ipfs(file_bytes, filename="image.png"):
    response = requests.post(
        PINATA_BASE_URL + "pinFileToIPFS",
        files={"file": (filename, file_bytes)},
        headers={
            "pinata_api_key": PINATA_API_KEY,
            "pinata_secret_api_key": PINATA_SECRET_API_KEY
        }
    )
    response.raise_for_status()
    return response.json()["IpfsHash"]

def upload_json_to_ipfs(metadata: dict):
    response = requests.post(
        PINATA_BASE_URL + "pinJSONToIPFS",
        json=metadata,
        headers={
            "pinata_api_key": PINATA_API_KEY,
            "pinata_secret_api_key": PINATA_SECRET_API_KEY,
            "Content-Type": "application/json"
        }
    )
    response.raise_for_status()
    return response.json()["IpfsHash"]
