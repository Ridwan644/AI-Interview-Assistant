from pydantic import BaseModel 
from datetime import datetime
class InterviewCreate(BaseModel): 
    interview_type: str 

class InterviewResponse(BaseModel):
    id: int
    user_id: int
    interview_type: str
    status: str
    started_at: datetime 
    class Config:
        from_attributes = True