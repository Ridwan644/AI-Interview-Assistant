from fastapi import FastAPI 
from app.routers import learn

from app.routers import interviews 
from app.routers import users 
#this single object is your entire API.
#Every route, every endpoint attaches to it. 
#when the server runs, its running this app 
app = FastAPI() 

@app.get("/")
def read_root():
    return{"message": "Interview Asistant API is running"}

app.include_router(learn.router)
app.include_router(interviews.router)
app.include_router(users.router)
