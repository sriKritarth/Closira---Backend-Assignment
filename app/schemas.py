from pydantic import BaseModel , Field
from typing import Literal


class CreateEnquiryRequest(BaseModel):
    channel : Literal['whatsApp' , 'email' , 'call'] = Field(... , description="Channels from which enquiry is recieved")
    customer_name : str = Field(... ,min_length=2 , max_length = 100 ,  description = "Name of the customer sending the enquiry")
    message : str = Field(... ,min_length= 5 , max_length=1000 ,  description="Customer enquiry message")


class CreateEnquiryResponse(BaseModel):
    job_id : int = Field(... , description = "Unique ID of the created enquiry/background job")
    status : Literal['processing'] = Field(... ,description= "Current enquiry processing status")
    message : str = Field(... , description = "Confirmation message")