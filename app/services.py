from app.crud import get_enquiry_by_id , update_enquiry_after_sop_match , create_enquiry_event , auto_escalate_enquiry
from app.sop_matcher import match_sop


def process_enquiry(enquiry_id):

    enquiry = get_enquiry_by_id(enquiry_id)

    if not enquiry:
        return
    
    message = enquiry["message"]

    res = match_sop(message)

    if not res:
        auto_escalate_enquiry(enquiry_id)
        create_enquiry_event(
            enquiry_id,
            "auto_escalated",
            "No SOP matched. Enquiry escalated to human agent."
        )
        create_enquiry_event(
            enquiry_id,
            "task_processed",
            "Background task completed with auto escalation."
        )
        return
    
    update_enquiry_after_sop_match(enquiry_id , res['matched_sop'] , res['suggested_response'])
    
    create_enquiry_event(
        enquiry_id,
        "sop_matched",
        f"SOP matched: {res['matched_sop']}",
        f"matched_keyword={res['matched_keyword']}"
    )

    create_enquiry_event(
        enquiry_id,
        "task_processed",
        "Background task completed successfully."
    )

    return
        
