from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.learn import Learn
from app.schemas.learn import LearnListItem 

#creates a router 
#(a mini app that holds this group of related endpoints)

router = APIRouter()

#When a GET request hits/learn run this function below 
@router.get("/learn", response_model=list[LearnListItem])

#the function that handles the request 
#bfore running me,call get_db
#get a database session, and hand it to me as db. 
def get_learn_topics(db: Session = Depends(get_db)): 
    #uses the session to query the database 
    #gets all rows from the Learn table 
    #returns a list of full Learn objects 
    learn = db.query(Learn).all()
    return learn



'''
THE WHOLE PURPOSE: 
The endpoint lets a user request the list of available learn topics. 
When they hit GET/learn, it opens a datbase session
fetches all learn topics from the table 
filters each down to the lightwiehg tlist shape (title/topic, no heavy content) 
returns them as JSON, the "menu" of lessons they can click into

'''
