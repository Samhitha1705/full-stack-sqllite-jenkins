from db import get_db
from datetime import datetime

def ensure_last_login_column(cur):
    cur.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cur.fetchall()]
    if "last_login" not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN last_login TEXT")
        print("Added 'last_login' column to users table.")

def update_all_users_last_login():
    conn = get_db()
    cur = conn.cursor()

    ensure_last_login_column(cur)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("UPDATE users SET last_login = ? WHERE last_login IS NULL", (now,))

    conn.commit()
    conn.close()
    print("✅ All users now have last_login set (if missing)")

if __name__ == "__main__":
    update_all_users_last_login()
