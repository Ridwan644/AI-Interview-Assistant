from app.db.database import SessionLocal
from app.models.user import User   

db = SessionLocal() 

fakeUser1 = User(
    clerk_user_id ="test_user_001",
    name="Johnathan",
    major="Computer Science", 
    target_role="Software Engineer", 
    target_company="johnson and johnson"
)


fakeUser2 = User(
    clerk_user_id="test_user_002",
    name="Awais",
    major="Data Science", 
    target_role="Data Scientist", 
    target_company="Amazon"
)


db.add(fakeUser1)
db.add(fakeUser2)

db.commit()
db.close()