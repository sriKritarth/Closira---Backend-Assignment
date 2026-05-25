from pydantic import BaseModel , Field
from typing import Literal , Optional


class CreateEnquiryRequest(BaseModel):
    channel : Literal['whatsapp' , 'email' , 'call'] = Field(... , description="Channels from which enquiry is recieved")
    customer_name : str = Field(... ,min_length=2 , max_length = 100 ,  description = "Name of the customer sending the enquiry")
    message : str = Field(... ,min_length= 5 , max_length=1000 ,  description="Customer enquiry message")


class CreateEnquiryResponse(BaseModel):
    job_id : int = Field(... , description = "Unique ID of the created enquiry/background job")
    status : Literal['processing'] = Field(... ,description= "Current enquiry processing status")
    message : str = Field(... , description = "Confirmation message")


class FollowUpRequest(BaseModel):
    delay_minutes: int = Field(... , gt=0, le=10080,
        description="Delay in minutes after which follow-up should be scheduled",
     
    )
    message_template: Optional[str] = Field(
        None,
        max_length=1000,
        description="Optional follow-up message template",
    )


class EscalationRequest(BaseModel):
    reason : str = Field(... , min_length=5 , max_length= 500 , description="Reason for escalating the enquiry to a human agent")