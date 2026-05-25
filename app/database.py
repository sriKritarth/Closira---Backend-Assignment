import sqlite3
from pathlib import Path

_DB_PATH = str(Path(__file__).parent.parent/"data.db")


def get_connection():
    conn = sqlite3.connect(_DB_PATH , check_same_thread=False)
    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_connection()

    with conn :
        conn.execute(
            
            """
            CREATE TABLE IF NOT EXISTS enquiries(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel TEXT NOT NULL,
                customer_name TEXT NOT NULL,
                message TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'processing',
                matched_sop TEXT,
                suggested_response TEXT,
                escalation_reason TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            """
        )


        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS enquiry_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enquiry_id INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                description TEXT NOT NULL,
                event_metadata TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (enquiry_id) REFERENCES enquiries(id)
            );
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS follow_ups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enquiry_id INTEGER NOT NULL,
                delay_minutes INTEGER NOT NULL,
                message_template TEXT,
                scheduled_for TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'scheduled',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (enquiry_id) REFERENCES enquiries(id)
            );

            """
        )
        
    conn.close()
