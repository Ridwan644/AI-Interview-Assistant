from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
from app.db.database import get_db 
from app.models.user import User
from app.schemas.user import UserUpdate, UserResponse

router = APIRouter() 

@router.patch("/users/me", response_model=UserResponse)
def update_user(user_update: UserUpdate, db: Session = Depends(get_db)): 
    #1.Find the user (hardcoded test user for now)
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        raise HTTPException(status_code=404, detail ="User not found")
    
    #2.update only the fields that were sent 
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items(): 
        setattr(user, field, value)
        
    #save and return
    db.commit()
    db.refresh(user)
    return user 