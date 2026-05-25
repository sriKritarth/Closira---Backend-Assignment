from app.database import get_connection
import sqlite3


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
    
    


