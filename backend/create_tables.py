from sqlalchemy import create_engine 
from sqlalchemy.orm import declarative_base
from app.models.learn import Learn
from app.db.database import Base, engine 


#base.metdaata is where Base keeps its list of tabels 
#the "paper iwth your drawing lives on Base"
#.create(all..)the build everything on paper command 
#bind = engine tells it which database to build in 
Base.metadata.create_all(bind=engine)
