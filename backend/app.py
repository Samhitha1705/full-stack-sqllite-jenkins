from flask import Flask, request, jsonify, send_from_directory
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR)

# --------------------------
# Serve Frontend Pages
# --------------------------
@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/dashboard")
def dashboard():
    return send_from_directory(FRONTEND_DIR, "dashboard.html")

@app.route("/auth.js")
def js():
    return send_from_directory(FRONTEND_DIR, "auth.js")

@app.route("/style.css")
def css():
    return send_from_directory(FRONTEND_DIR, "style.css")

# --------------------------
# Register API
# --------------------------
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT
        )
    """)
    # Check if username exists
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    if cur.fetchone():
        conn.close()
        return jsonify({"error": "Username already exists"}), 400

    # Hash password
    hash_pwd = generate_password_hash(password)
    cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hash_pwd))
    conn.commit()
    conn.close()
    return jsonify({"message": "User registered successfully"})

# --------------------------
# Login API
# --------------------------
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    if not user or not check_password_hash(user[1], password):
        conn.close()
        return jsonify({"error": "Invalid credentials"}), 401

    # Store login history
    cur.execute("""
        CREATE TABLE IF NOT EXISTS logins (
            id INTEGER PRIMARY KEY,
            username TEXT,
            login_time TEXT
        )
    """)
    cur.execute("INSERT INTO logins (username, login_time) VALUES (?, ?)", (username, datetime.now().isoformat()))
    conn.commit()
    conn.close()

    return jsonify({"message": f"{username} logged in successfully!"})

# --------------------------
# Login History API
# --------------------------
@app.route("/api/logins")
def logins():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT username, login_time FROM logins ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"username": r[0], "time": r[1]} for r in rows])

# --------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
