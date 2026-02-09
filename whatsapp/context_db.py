import sqlite3
from pathlib import Path

# DB file
DB_PATH = Path(__file__).resolve().parent / "chat_memory.db"

# Initialize DB
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_number TEXT,
    role TEXT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
conn.close()


def add_message(user_number: str, role: str, message: str):
    """Add a message to the DB."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO messages (user_number, role, message) VALUES (?, ?, ?)",
        (user_number, role, message)
    )
    conn.commit()
    conn.close()


def get_history(user_number: str, limit: int = 10):
    """Retrieve last N messages for a user."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT role, message FROM messages WHERE user_number=? ORDER BY id DESC LIMIT ?",
        (user_number, limit)
    )
    rows = c.fetchall()
    conn.close()
    # Return messages in chronological order
    return [{"role": r[0], "content": r[1]} for r in reversed(rows)]
