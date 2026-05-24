from fastapi import APIRouter 
from app.schemas import CreateEnquiryRequest , CreateEnquiryResponse
from app.crud import create_enquiry , create_enquiry_event


router_enquiry = APIRouter()

@router_enquiry.post("/enquiry" ,response_model=CreateEnquiryResponse)
async def create_new_enquiry(enq_schema : CreateEnquiryRequest):
    channel = enq_schema.channel
    customer_name = enq_schema.customer_name
    message = enq_schema.message
    
    enquiry_id = create_enquiry(channel , customer_name , message)

    create_enquiry_event(enquiry_id , "enquiry_created" , "New enquiry received from customer")

    
    return {
        "job_id" : enquiry_id,
        "status" :"processing",
        "message" : "Enquiry received and queued for processing"
    }
    
