from fastapi import FastAPI, HTTPException, Depends, APIRouter
from pydantic_model import user,response, user_details, user_details_response
from random import randrange
from fastapi.responses import JSONResponse
from fastapi import status
from typing import List
from database import engine, get_db
import model_database
from sqlalchemy.orm import Session
from utils import hash_password

router = APIRouter(
     tags=["users"]
)

@router.post("/create_user", status_code=201, response_model=user_details_response)
async def create_user(user: user_details, db: Session = Depends(get_db)):
     hashed_password = hash_password(user.password)
     user.password = hashed_password
     new_user=model_database.UserDetails(**user.model_dump())
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     return new_user

@router.get("/get_users/{user_id}", status_code=200, response_model=user_details_response)
async def get_users(user_id: int,db: Session = Depends(get_db)):
    user=db.query(model_database.UserDetails).filter(model_database.UserDetails.id==user_id).first()
    return user