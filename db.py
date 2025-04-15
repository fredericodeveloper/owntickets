# db.py

import sqlite3

# Private global conn (you'll expose it via a getter)
_conn = None

def table_exists(table_name):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    return bool(cursor.fetchone())

def init_db():
    global _conn
    _conn = sqlite3.connect('owntickets.db')
    cursor = _conn.cursor()
    if not table_exists("app_data"):
        # Runs this section if it never been ran before
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_data (
                key VARCHAR(100) NOT NULL UNIQUE,
                value TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS server_info (
                server_id INTEGER PRIMARY KEY UNIQUE,
                open_ticket_channel_id VARCHAR(100),
                open_ticket_message_id VARCHAR(100),
                language VARCHAR(50)
            )
        ''')

    _conn.commit()

def get_conn():
    global _conn
    if _conn is None:
        raise RuntimeError("Database not initialized. Call db.init_db() first.")
    return _conn
