import os
import libsql_experimental as libsql

conn = libsql.connect(
    os.getenv("TURSO_DB_URL"),
    auth_token=os.getenv("TURSO_AUTH_TOKEN")
)

conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    language_code TEXT,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

def log_user(user):
    conn.execute(
        "INSERT OR IGNORE INTO users (user_id, username, first_name, language_code) VALUES (?, ?, ?, ?)",
        (user.id, user.username, user.first_name, user.language_code)
    )
    conn.commit()