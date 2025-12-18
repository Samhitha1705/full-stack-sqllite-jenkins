from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="")
app.secret_key = "supersecretkey"  # required for session

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "app.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("../frontend", path)

# Login API
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    conn = get_db()
    cur = conn.cursor()
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

    session['username'] = username
    conn.close()
    return jsonify({"message": message}), 200

# Logout API
@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop('username', None)
    return jsonify({"message": "Logged out successfully"}), 200

# Dashboard page
@app.route("/dashboard")
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    return send_from_directory("../frontend", "dashboard.html")

# API to get users
@app.route("/api/users", methods=["GET"])
def get_users():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username FROM users")
    users = cur.fetchall()
    conn.close()
    users_list = [{"id": u["id"], "username": u["username"]} for u in users]
    return jsonify({"users": users_list})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
