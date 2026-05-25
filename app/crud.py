from app.database import get_connection
import sqlite3
from typing import Optional
import time
from datetime import timedelta , datetime , timezone


def create_enquiry(channel , customer_name , message ):
    conn = get_connection()
    curr = conn.cursor()
    curr.execute(
        """
        INSERT INTO enquiries(channel , customer_name , message ) VALUES(? ,? , ? )
        """ , (channel , customer_name , message ))
    
    enquiry_id =curr.lastrowid
    conn.commit()


    conn.close()

    return enquiry_id

def create_enquiry_event(enquiry_id , event_type ,description ,  event_metadata = None):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO enquiry_events(enquiry_id , event_type , description , event_metadata) VALUES(? , ? , ? , ?)
        """ , (enquiry_id , event_type , description , event_metadata))
    
    conn.commit()
    conn.close()


def get_enquiry_by_id(enquiry_id) -> sqlite3.Row:
    conn = get_connection()

    enquiry = conn.execute(
        """
        SELECT * FROM enquiries where id = ? 
        """ , (enquiry_id,)).fetchone()
    

    conn.close()
    
    return enquiry

def update_enquiry_after_sop_match(enquiry_id, matched_sop, suggested_response):
    conn = get_connection()

    conn.execute(
        """
        UPDATE enquiries
        SET 
            status = ?,
            matched_sop = ?,
            suggested_response = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        ("qualified", matched_sop, suggested_response, enquiry_id)
    )

    conn.commit()
    conn.close()


def auto_escalate_enquiry(enquiry_id, reason="No matching SOP found"):
    conn = get_connection()

    conn.execute(
        """
        UPDATE enquiries
        SET 
            status = ?,
            escalation_reason = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        ("escalated", reason, enquiry_id)
    )

    conn.commit()
    conn.close()


def row_to_dict(row):
    if row is None:
        return None
    return dict(row)


def rows_to_dicts(rows):
    return [dict(row) for row in rows]


def get_events_by_enquiry_id(enquiry_id: int):
    conn = get_connection()

    events = conn.execute(
        """
        SELECT id, enquiry_id, event_type, description, event_metadata, created_at
        FROM enquiry_events
        WHERE enquiry_id = ?
        ORDER BY created_at ASC, id ASC
        """,
        (enquiry_id,),
    ).fetchall()

    conn.close()
    return events


def get_follow_ups_by_enquiry_id(enquiry_id: int):
    conn = get_connection()

    follow_ups = conn.execute(
        """
        SELECT id, enquiry_id, delay_minutes, message_template, scheduled_for, status, created_at
        FROM follow_ups
        WHERE enquiry_id = ?
        ORDER BY scheduled_for ASC, id ASC
        """,
        (enquiry_id,),
    ).fetchall()

    conn.close()
    return follow_ups


def create_follow_up(enquiry_id: int, delay_minutes: int, message_template: Optional[str] = None):
    scheduled_for = (datetime.now(timezone.utc)  + timedelta(minutes=delay_minutes)).strftime("%Y-%m-%d %H:%M UTC")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO follow_ups(enquiry_id, delay_minutes, message_template, scheduled_for, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (enquiry_id, delay_minutes, message_template, scheduled_for, "scheduled"),
    )

    follow_up_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return follow_up_id, scheduled_for


def update_enquiry_status(enquiry_id: int, status: str):
    conn = get_connection()

    conn.execute(
        """
        UPDATE enquiries
        SET status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (status, enquiry_id),
    )

    conn.commit()
    conn.close()

