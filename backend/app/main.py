from fastapi import FastAPI 

#this single object is your entire API.
#Every route, every endpoint attaches to it. 
#when the server runs, its running this app 
app = FastAPI() 

@app.get("/")
def read_root():
    return{"message": "Interview Asistant API is running"}
