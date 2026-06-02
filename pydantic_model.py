from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime
class user(BaseModel):
    title: str
    content: str
    published: bool = True



    class Config:
        from_attributes = True 


class user_details(BaseModel):
    email: str
    password: str        

class user_details_response(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class response(BaseModel):
    id: int
    title: str
    content: str
    published: bool   
    created_at: datetime
    user_id: int
    owner: user_details_response

    class Config:
        from_attributes = True

class vote_response(BaseModel):
    Post: response
    votes: int

    class Config:
        from_attributes = True




class user_login(BaseModel):
    email: EmailStr
    password: str        

class token(BaseModel):
    access_token: str
    token_type: str

class token_data(BaseModel):
    id: Optional[str]=None

class vote(BaseModel):
    post_id: int
    dir: Literal[0,1]