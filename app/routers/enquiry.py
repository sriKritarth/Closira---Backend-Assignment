from fastapi import APIRouter , BackgroundTasks , HTTPException
from app.schemas import (
    CreateEnquiryRequest , 
    CreateEnquiryResponse
)
from app.crud import (
    create_enquiry , 
    create_enquiry_event ,
    get_enquiry_by_id , 
    get_events_by_enquiry_id , 
    get_follow_ups_by_enquiry_id,
    row_to_dict , 
    rows_to_dicts
)
from app.services import process_enquiry


router_enquiry = APIRouter()

@router_enquiry.post("/enquiry" ,response_model=CreateEnquiryResponse)
async def create_new_enquiry(enq_schema : CreateEnquiryRequest , background_task : BackgroundTasks):
    channel = enq_schema.channel
    customer_name = enq_schema.customer_name
    message = enq_schema.message
    
    enquiry_id = create_enquiry(channel , customer_name , message)

    create_enquiry_event(enquiry_id , "enquiry_created" , "New enquiry received from customer")

    background_task.add_task(process_enquiry ,enquiry_id)

    
    return {
        "job_id" : enquiry_id,
        "status" :"processing",
        "message" : "Enquiry received and queued for processing"
    }

@router_enquiry.get("/enquiry/{enquiry_id}/history")
async def get_enquiry_history(enquiry_id: int):
    enquiry = get_enquiry_by_id(enquiry_id)

    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")

    events = get_events_by_enquiry_id(enquiry_id)
    follow_ups = get_follow_ups_by_enquiry_id(enquiry_id)

    return {
        "enquiry": row_to_dict(enquiry),
        "timeline": rows_to_dicts(events),
        "follow_ups": rows_to_dicts(follow_ups),
    }
