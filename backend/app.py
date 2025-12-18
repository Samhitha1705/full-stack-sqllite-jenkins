from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

# Set up Flask app
app = Flask(__name__, static_folder="../frontend", static_url_path="")

# Ensure data folder exists
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "app.db")

# Function to get DB connection
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Serve frontend
@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("../frontend", path)

# Login API (auto-register if user not exists)
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    conn = get_db()
    cur = conn.cursor()

    # Create table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT
        )
    """)

    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()

    if not user:
        # Auto-register
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, generate_password_hash(password))
        )
        conn.commit()
        message = "User auto-registered and logged in"
    else:
        if not check_password_hash(user["password_hash"], password):
            conn.close()
            return jsonify({"error": "Invalid credentials"}), 401
        message = "Login successful"

    conn.close()
    return jsonify({"message": message}), 200

# API to fetch users for dashboard
@app.route("/api/users", methods=["GET"])
def get_users():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash FROM users")
    users = cur.fetchall()
    conn.close()
    users_list = [{"id": u["id"], "username": u["username"], "password": u["password_hash"]} for u in users]
    return jsonify({"users": users_list})

# Dashboard page
@app.route("/dashboard")
def dashboard():
    return send_from_directory("../frontend", "dashboard.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
