import sqlite3
from datetime import datetime
from app.models import get_db_connection


def insert_message(message):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO messages (message_id, from_msisdn, to_msisdn, ts, text, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            message["message_id"],
            message["from"],
            message["to"],
            message["ts"],
            message.get("text"),
            datetime.utcnow().isoformat() + "Z"
        ))
        conn.commit()
        return "created"
    except sqlite3.IntegrityError:
        # duplicate message_id
        return "duplicate"
    finally:
        conn.close()
