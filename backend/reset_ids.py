from db import DB_PATH
import sqlite3

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create a new table
cur.execute("""
CREATE TABLE new_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT,
    last_login TEXT
)
""")

# Copy existing users
cur.execute("SELECT username, password_hash, last_login FROM users ORDER BY id")
users = cur.fetchall()
for user in users:
    cur.execute("INSERT INTO new_users (username, password_hash, last_login) VALUES (?, ?, ?)",
                (user[0], user[1], user[2]))

# Replace old table
cur.execute("DROP TABLE users")
cur.execute("ALTER TABLE new_users RENAME TO users")

conn.commit()
conn.close()
print("✅ User IDs reset to contiguous numbers.")
