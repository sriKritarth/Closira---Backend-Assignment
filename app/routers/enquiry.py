from fastapi import APIRouter , BackgroundTasks
from app.schemas import CreateEnquiryRequest , CreateEnquiryResponse
from app.crud import create_enquiry , create_enquiry_event
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
