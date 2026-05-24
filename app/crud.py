from app.database import get_connection


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
    


