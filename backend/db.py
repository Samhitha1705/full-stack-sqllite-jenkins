import sqlite3
import os

DB_DIR = "/app/data"
DB_PATH = os.path.join(DB_DIR, "app.db")

def get_db():
    # Ensure data directory exists
    os.makedirs(DB_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
