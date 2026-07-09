from pydantic import BaseModel 

class LearnListItem(BaseModel): 
    id: int 
    title: str 
    topic: str 
    #does content have to be str? 
    #yes it does 
    #the model stores as text, but when it comes to python it's jsut a string, so schema says str 
    #the model speaks SQL (text), schema speakas Python 
    #content: str

    class Config: 
        from_attributes = True 

class LearnDetail(BaseModel):
    id: int 
    title: str 
    topic: str 
    #does content have to be str? 
    #yes it does 
    #the model stores as text, but when it comes to python it's jsut a string, so schema says str 
    #the model speaks SQL (text), schema speakas Python 
    content: str

    class Config: 
        from_attributes = True 