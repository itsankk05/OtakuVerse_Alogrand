import os
import sqlite3

# Set DB path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "anime.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def save_anime_to_db(metadata, cid, creator_wallet):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO anime_metadata (title, description, episodes, thumbnail, status, ipfs_cid, created_at)
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
    """,
        (
            metadata["title"],
            metadata["description"],
            metadata["episodes"],
            metadata["thumbnail"],
            metadata["status"],
            cid,
        ),
    )
    anime_id = cursor.lastrowid

    for nft in metadata.get("nftCollection", []):
        cursor.execute(
            """
            INSERT INTO anime_nfts (anime_id, name, image, episode, watch_time, rarity, is_listed, minted_at, creator_address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                anime_id,
                nft["name"],
                nft["image"],
                nft["episode"],
                nft["watchTime"],
                nft["rarity"],
                nft["isListed"],
                nft["mintedAt"],
                creator_wallet,
            ),
        )

    conn.commit()
    conn.close()


def fetch_all_anime_with_nfts():
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch all anime entries
    cursor.execute(
        """
        SELECT id, title, description, episodes, thumbnail, status, ipfs_cid, created_at
        FROM anime_metadata
    """
    )
    anime_rows = cursor.fetchall()

    anime_list = []

    for row in anime_rows:
        anime_id = row[0]

        # Fetch related NFTs
        cursor.execute(
            """
            SELECT id, name, image, episode, watch_time, rarity, is_listed, minted_at, creator_address
            FROM anime_nfts
            WHERE anime_id = ?
        """,
            (anime_id,),
        )
        nft_rows = cursor.fetchall()

        nfts = []
        for nft in nft_rows:
            nfts.append(
                {
                    "id": nft[0],
                    "name": nft[1],
                    "image": nft[2],
                    "episode": nft[3],
                    "watchTime": nft[4],
                    "rarity": nft[5],
                    "isListed": bool(nft[6]),
                    "mintedAt": nft[7],
                    "creatorAddress": nft[8],
                }
            )

        anime_list.append(
            {
                "id": anime_id,
                "title": row[1],
                "description": row[2],
                "episodes": row[3],
                "thumbnail": row[4],
                "status": row[5],
                "ipfs_cid": row[6],
                "created_at": row[7],
                "nftCollection": nfts,
            }
        )

    conn.close()
    return anime_list


def store_user_contract_mapping(wallet_address: str, app_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_contracts (
                wallet TEXT NOT NULL,
                app_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (wallet, app_id)
        )
    """
    )
    cursor.execute(
        """
        INSERT INTO user_contracts (wallet, app_id)
        VALUES (?, ?)
    """,
        (wallet_address, app_id),
    )
    conn.commit()
    conn.close()
