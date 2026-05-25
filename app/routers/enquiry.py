import json
from fastapi import APIRouter , BackgroundTasks , HTTPException
from app.schemas import (
    CreateEnquiryRequest , 
    CreateEnquiryResponse, 
    FollowUpRequest
)
from app.crud import (
    create_enquiry , 
    create_enquiry_event ,
    get_enquiry_by_id , 
    get_events_by_enquiry_id , 
    get_follow_ups_by_enquiry_id,
    row_to_dict , 
    rows_to_dicts,
    update_enquiry_status ,
    create_follow_up
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

@router_enquiry.post("/enquiry/{enquiry_id}/follow-up")
async def schedule_follow_up(enquiry_id: int, payload: FollowUpRequest):
    enquiry = get_enquiry_by_id(enquiry_id)

    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")

    if enquiry["status"] in ["escalated", "closed"]:
        raise HTTPException(
            status_code=400,
            detail="Cannot schedule follow-up for an escalated or closed enquiry",
        )

    follow_up_id, scheduled_for = create_follow_up(
        enquiry_id=enquiry_id,
        delay_minutes=payload.delay_minutes,
        message_template=payload.message_template,
    )

    update_enquiry_status(enquiry_id, "follow_up_scheduled")

    create_enquiry_event(
        enquiry_id,
        "follow_up_scheduled",
        "Follow-up scheduled for enquiry",
        json.dumps(
            {
                "follow_up_id": follow_up_id,
                "delay_minutes": payload.delay_minutes,
                "scheduled_for": scheduled_for,
            }
        ),
    )

    return {
        "follow_up_id": follow_up_id,
        "enquiry_id": enquiry_id,
        "status": "follow_up_scheduled",
        "scheduled_for": scheduled_for,
        "message": "Follow-up scheduled successfully",
    }


