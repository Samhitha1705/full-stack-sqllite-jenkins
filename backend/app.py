from flask import Flask, request, jsonify, send_from_directory, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

# Set up Flask app
app = Flask(__name__, static_folder="../frontend", static_url_path="")
app.secret_key = "supersecretkey"

# Ensure data folder exists
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "app.db")

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
                font-family: 'Comic Sans MS', cursive, sans-serif;
                background: linear-gradient(120deg, #f6d365, #fda085);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                animation: fadeIn 1s ease-in;
            }}
            @keyframes fadeIn {{
                from {{opacity: 0;}}
                to {{opacity: 1;}}
            }}
            h1 {{
                color: #fff;
                text-shadow: 2px 2px 5px #ff6f91;
            }}
            form {{
                background-color: rgba(255,255,255,0.9);
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.3);
                display: flex;
                flex-direction: column;
                width: 320px;
                animation: slideUp 0.5s ease-out;
            }}
            @keyframes slideUp {{
                from {{transform: translateY(50px); opacity:0;}}
                to {{transform: translateY(0); opacity:1;}}
            }}
            input {{
                padding: 12px;
                margin: 10px 0;
                border-radius: 12px;
                border: 1px solid #ddd;
                font-size: 16px;
            }}
            button {{
                background-color: #ff6f91;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 12px;
                cursor: pointer;
                font-size: 16px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            }}
            button:hover {{
                background-color: #ff4f70;
                transform: scale(1.05) rotate(-2deg);
                box-shadow: 0 6px 15px rgba(0,0,0,0.3);
            }}
            .message {{
                color: green;
                text-align: center;
                margin-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>✨ Login ✨</h1>
        <form method="POST" action="/api/login">
            <div class="message">{message}</div>
            <input type="text" name="username" placeholder="Username" required />
            <input type="password" name="password" placeholder="Password" required />
            <button type="submit">Login 🔑</button>
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
        <title>🎉 Dashboard - Users 🎉</title>
        <style>
            body {{
                font-family: 'Comic Sans MS', cursive, sans-serif;
                background: linear-gradient(120deg, #a1c4fd, #c2e9fb);
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 40px;
                animation: fadeIn 1s ease-in;
            }}
            @keyframes fadeIn {{
                from {{opacity: 0;}}
                to {{opacity: 1;}}
            }}
            h1 {{
                color: #ff6f91;
                text-shadow: 2px 2px 5px #fff;
                animation: bounce 1s infinite;
            }}
            @keyframes bounce {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-10px); }}
            }}
            .user-card {{
                background: linear-gradient(135deg, #ff9a9e, #fad0c4);
                border-radius: 20px;
                padding: 20px;
                margin: 15px;
                width: 220px;
                text-align: center;
                font-size: 18px;
                color: #fff;
                font-weight: bold;
                box-shadow: 0 8px 15px rgba(0,0,0,0.2);
                transition: transform 0.3s, box-shadow 0.3s;
            }}
            .user-card:hover {{
                transform: translateY(-5px) scale(1.05);
                box-shadow: 0 12px 20px rgba(0,0,0,0.3);
            }}
            .logout-btn {{
                background: #ff6f91;
                color: white;
                padding: 12px 25px;
                border: none;
                border-radius: 15px;
                cursor: pointer;
                font-size: 18px;
                margin-top: 20px;
                transition: all 0.3s ease;
            }}
            .logout-btn:hover {{
                background: #ff4f70;
                transform: scale(1.1) rotate(-3deg);
            }}
        </style>
    </head>
    <body>
        <h1>🎈 Dashboard 🎈</h1>
    """

    for u in users_list:
        html += f'<div class="user-card">👤 {u["username"]} <br> 🆔 {u["id"]}</div>'

    html += """
        <form method="POST" action="/logout">
            <button class="logout-btn">Logout 🚪</button>
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
