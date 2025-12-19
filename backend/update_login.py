from db import get_db
from datetime import datetime

def ensure_last_login_column(cur):
    """Ensure the 'last_login' column exists in the users table."""
    cur.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cur.fetchall()]
    if "last_login" not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN last_login TEXT")
        print("Added 'last_login' column to users table.")

def update_all_users_last_login():
    """Update last_login for all users to current datetime."""
    conn = get_db()
    cur = conn.cursor()

    # Ensure the last_login column exists
    ensure_last_login_column(cur)

    # Get all usernames
    cur.execute("SELECT username FROM users")
    users = cur.fetchall()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for user in users:
        username = user["username"]
        cur.execute("UPDATE users SET last_login = ? WHERE username = ?", (now, username))
        print(f"{username} last_login updated to {now}")

    conn.commit()
    conn.close()
    print("All users' last_login updated successfully!")

if __name__ == "__main__":
    update_all_users_last_login()
