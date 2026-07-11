from sqlalchemy import Column, Integer, String, DateTime, ForeignKey 
from sqlalchemy.sql import func 
from app.db.database import Base 

class MockInterview(Base):
    __tablename__ = "mock_interviews"
    
    id = Column(Integer, primary_key = True, index = True) 
    
    user_id = Column(Integer, ForeignKey("users.id"), index = True, nullable = False)
    
    interview_type = Column(String(250), nullable = False)
    status = Column(String(250), nullable=False, default="in_progress")    
    
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)       
    

    #timestamp 
