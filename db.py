import sqlite3
import os

# Absolute path to the program folder
PROGRAM_DIR = os.path.expanduser("~/.programs/habits")
DB_FILE = os.path.join(PROGRAM_DIR, "habits.db")

# Make sure the folder exists
os.makedirs(PROGRAM_DIR, exist_ok=True)

def get_conn():
    """Return a connection to the SQLite database."""
    return sqlite3.connect(DB_FILE)

def init_db():
    """Initialize the database with required tables and columns."""
    conn = get_conn()
    cur = conn.cursor()

    # Create habits table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        created_at TEXT
    )
    """)

    # Create streak_history table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS streak_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER,
        streak_length TEXT,
        fail_date TEXT
    )
    """)

    # Check if 'reason' column exists, add if missing
    cur.execute("PRAGMA table_info(streak_history)")
    columns = [col[1] for col in cur.fetchall()]
    if "reason" not in columns:
        cur.execute("ALTER TABLE streak_history ADD COLUMN reason TEXT")

    # Create current_streak table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS current_streak (
        habit_id INTEGER PRIMARY KEY,
        start_datetime TEXT
    )
    """)

    conn.commit()
    conn.close()