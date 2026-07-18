from pydantic import BaseModel 

class UserUpdate(BaseModel): 
    name: str | None = None
    major: str | None = None
    target_role: str | None = None
    target_company: str | None = None
    
class UserResponse(BaseModel): 
    id: int 
    name: str | None = None
    major: str | None = None
    target_role: str | None = None
    target_company: str | None = None
    class Config: 
        from_attributes = True 