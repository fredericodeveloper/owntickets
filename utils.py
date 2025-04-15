import db

def set_ticket_message_id(server_id: int, message_id: str):
    conn = db.get_conn()
    cursor = conn.cursor()
    count = cursor.execute("SELECT COUNT(*) FROM server_info WHERE server_id = ?", (server_id,)).fetchone()[0]

    # If server is not already initialized
    if count == 0:
        return False

    # If server is already initialized
    cursor.execute("""
        UPDATE server_info SET open_ticket_message_id = ? WHERE server_id = ?
    """, (message_id, server_id))

    conn.commit()

    return True

def get_ticket_channel_message_info(server_id: int):
    conn = db.get_conn()
    cursor = conn.cursor()
    result = cursor.execute("SELECT open_ticket_channel_id, open_ticket_message_id FROM server_info WHERE server_id = ?", (server_id,)).fetchone()

    if result:
        return result[0], result[1]
    else:
        return None, None

def unset_initialized(server_id: int):
    conn = db.get_conn()
    cursor = conn.cursor()
    count = cursor.execute("SELECT COUNT(*) FROM server_info WHERE server_id = ?", (server_id,)).fetchone()[0]

    # If server is already uninitialized
    if count == 0:
        return False

    # If server is initialized
    cursor.execute("""
        DELETE FROM server_info WHERE server_id = ?
    """, (server_id,))

    conn.commit()

    return True

def set_initialized(server_id: int, channel_id: int, language: str):
    conn = db.get_conn()
    cursor = conn.cursor()
    count = cursor.execute("SELECT COUNT(*) FROM server_info WHERE server_id = ?", (server_id,)).fetchone()[0]

    # If server is already initilialized
    if count > 0:
        return False

    # If server is not already initialized
    cursor.execute("""
        INSERT INTO server_info (server_id, open_ticket_channel_id, language)
        VALUES (?, ?, ?)
    """, (server_id, channel_id, language))

    conn.commit()

    return True
