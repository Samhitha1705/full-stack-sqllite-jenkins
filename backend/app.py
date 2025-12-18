from flask import Flask, request, jsonify, send_from_directory, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

# Set up Flask app
app = Flask(__name__, static_folder="../frontend", static_url_path="")
app.secret_key = "supersecretkey"  # needed for session management

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

# Serve static frontend files
@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return login_page()

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("../frontend", path)

# Login Page
def login_page(message=""):
    return f"""
    <html>
    <head>
        <title>Login</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #ffe3e3;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
            }}
            h1 {{
                color: #ff6f91;
            }}
            form {{
                background-color: #fff;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
                display: flex;
                flex-direction: column;
                width: 300px;
            }}
            input {{
                padding: 10px;
                margin: 10px 0;
                border-radius: 10px;
                border: 1px solid #ddd;
            }}
            button {{
                background-color: #ff6f91;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                font-size: 16px;
                transition: background-color 0.3s;
            }}
            button:hover {{
                background-color: #ff4f70;
            }}
            .message {{
                color: green;
                text-align: center;
                margin-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>Login</h1>
        <form method="POST" action="/api/login">
            <div class="message">{message}</div>
            <input type="text" name="username" placeholder="Username" required />
            <input type="password" name="password" placeholder="Password" required />
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    """

# Login API
@app.route("/api/login", methods=["POST"])
def login():
    if request.is_json:
        data = request.json
        username = data.get("username")
        password = data.get("password")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

    if not username or not password:
        return login_page("Username and password required")

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
        # Auto-register
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, generate_password_hash(password))
        )
        conn.commit()
        session["username"] = username
        conn.close()
        return redirect(url_for("dashboard"))
    else:
        if not check_password_hash(user["password_hash"], password):
            conn.close()
            return login_page("Invalid credentials")
        session["username"] = username
        conn.close()
        return redirect(url_for("dashboard"))

# Dashboard route
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("index"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username FROM users")
    users = cur.fetchall()
    conn.close()

    users_list = [{"id": u["id"], "username": u["username"]} for u in users]

    html = """
    <html>
    <head>
        <title>Dashboard - Users</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f9f7f6;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 30px;
            }}
            h1 {{
                color: #ff6f91;
            }}
            .user-card {{
                background-color: #ffffff;
                border-radius: 12px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                padding: 20px;
                margin: 10px;
                width: 250px;
                text-align: center;
                transition: transform 0.2s, box-shadow 0.2s;
            }}
            .user-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            }}
            .logout-btn {{
                background-color: #ff6f91;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                margin-top: 20px;
                font-size: 16px;
            }}
            .logout-btn:hover {{
                background-color: #ff4f70;
            }}
        </style>
    </head>
    <body>
        <h1>Dashboard - Users</h1>
    """

    for u in users_list:
        html += f'<div class="user-card">ID: {u["id"]}<br>Username: {u["username"]}</div>'

    html += """
        <form method="POST" action="/logout">
            <button class="logout-btn">Logout</button>
        </form>
    </body>
    </html>
    """
    return html

# Logout
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
