from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func 

from app.db.database import Base 

class Learn(Base): 
    __tablename__ = "learn"
    
    id = column(Integer, primary_key = True, index=True)
    title = Column(String, nullable=False)