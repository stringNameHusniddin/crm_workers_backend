from pydantic import BaseModel, EmailStr
from typing import Optional, Union, List
from datetime import date

class WorksSchema(BaseModel):
    name : str
    join_data : date
    complete_data : date
    status : str
    to_id : int
    owner_id : int

class UserSchema(BaseModel):
    role : str
    username : str
    password: str
    first_name : str
    last_name : str
    join_data : date
    status : str
    age : int
    email : Union[EmailStr, None] = None
    boss_id:int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None    

class ShowUserWorks(BaseModel):
    id:int
    role : str
    username : str

class ShowWorks(BaseModel):
    id : int
    name : str
    join_data : date
    complete_data : date
    status : str
    owner : ShowUserWorks
    to : ShowUserWorks



class ShowWorksUser(BaseModel):
    id : int
    name : str
    join_data : date
    complete_data : date
    status : str
    to : ShowUserWorks
    owner : ShowUserWorks
    
    class Config:
        orm_mode = True

class Note(BaseModel):
    text : str
    owner_id : int

class ShowNote(BaseModel):
    id : int
    text : str
    owner : ShowUserWorks
    
    class Config:
        orm_mode = True

class ShowNoteUser(BaseModel):
    text : str

class Sub(BaseModel):
    username : str

class BaseNotifications(BaseModel):
    text : str

class createNotifications(BaseNotifications):
    owner_id : int
    to_id : int

class showNotifications(BaseNotifications):
    to : UserSchema
    owner : UserSchema

    class Config:
        orm_mode = True

class ShowUser(UserSchema):
    id:int
    works : List[ShowWorksUser]=[]
    created_works : List[ShowWorksUser]=[]
    notes : List[ShowNoteUser]=[]
    notifications : List[showNotifications]=[]
    created_notifications : List[showNotifications]=[]

    class Config:
        orm_mode = True