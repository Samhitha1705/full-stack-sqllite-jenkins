from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

# Set up Flask app
app = Flask(__name__, static_folder="../frontend", static_url_path="")

# Ensure data folder exists
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)  # create if not exists

DB_PATH = os.path.join(DATA_DIR, "app.db")  # database path inside data folder

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

# Dashboard route
@app.route("/dashboard")
def dashboard():
    return send_from_directory("../frontend", "dashboard.html")  # create dashboard.html in frontend folder

# Register API
@app.route("/api/register", methods=["POST"])
def register():
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

    try:
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, generate_password_hash(password))
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "User already exists"}), 400

    conn.close()
    return jsonify({"message": "User registered successfully"}), 201

# Login API
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Redirect to dashboard after login
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
