import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import sqlite3
from utils.db_utils import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS anime_metadata (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  description TEXT,
  episodes INTEGER,
  thumbnail TEXT,
  status TEXT,
  ipfs_cid TEXT,
  studio TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS anime_nfts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  anime_id INTEGER,
  name TEXT,
  image TEXT,
  episode INTEGER,
  watch_time INTEGER,
  rarity TEXT,
  is_listed BOOLEAN,
  minted_at TEXT,
  creator_address TEXT,
  FOREIGN KEY (anime_id) REFERENCES anime_metadata(id)
);
"""
)

conn.commit()
conn.close()
print("✅ Database initialized.")
