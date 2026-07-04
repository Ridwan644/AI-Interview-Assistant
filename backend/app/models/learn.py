from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey 
from sqlalchemy.sql import func 
from sqlalchemy.orm import relationship 
from app.db.database import Base 

'''
Using an orm(Object Relational Mapepr) 
What is an ORM?
An ORM lets you map python classes direclty to database tables and treat 
individual database rows as regular python objects 
'''

class Learn(Base): 
    __tablename__ = "learn"
    
    id = Column(Integer, primary_key=True, index=True)
    
    title = Column(String(255), unique=True, index=True, nullable=False)
    topic = Column(String(100), index=True, nullable=False)
    content = Column(Text,nullable=False)
    #timestamp 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
