from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func 
from app.db.database import Base 

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key = True, index = True) 
    
    clerk_user_id = Column(String(250), index = True, unique = True, nullable = False)
    
    name = Column(String(100), nullable = True)
    major = Column(String(100), nullable = True)
    target_role = Column(String(100),  nullable = True)
    target_company = Column(String(250), nullable = True)

    #timestamp 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    