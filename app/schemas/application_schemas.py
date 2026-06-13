from pydantic import BaseModel , ConfigDict , field_validator
from app.models.application_model import ApplicationStatus
from datetime import datetime




class ApplicationResponseModel(BaseModel):
    id:int
    user_id:int
    olympiad_id : int
    status : ApplicationStatus
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
class ApplicationUpdateStatusModel(BaseModel):
    status: ApplicationStatus
    
    
    @field_validator("status")
    @classmethod
    def validate_status(cls,value:ApplicationStatus):
        if value == ApplicationStatus.PENDING:
            raise ValueError("Aprrove or Reject the application")
            
        return value
    
class AdminApplicationResponseModel(BaseModel):
    id:int
    user_id:int
    olympiad_id : int
    status : ApplicationStatus
    created_at: datetime
    updated_at:datetime
    
    model_config = ConfigDict(from_attributes=True)
    
    