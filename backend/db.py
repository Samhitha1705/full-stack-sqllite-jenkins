import sqlite3
import os
import platform

# Determine data folder based on OS
if platform.system() == "Windows":
    DB_DIR = os.path.join(os.path.dirname(__file__), "data")  # backend/data
else:
    DB_DIR = "/app/data"  # Docker

os.makedirs(DB_DIR, exist_ok=True)  # Create folder if it doesn't exist
DB_PATH = os.path.join(DB_DIR, "app.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
