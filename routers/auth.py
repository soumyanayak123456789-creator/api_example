from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from utils import hash_password, verify
from pydantic_model import user_login, token
from oauth2 import create_token
import model_database
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=token)
async def login(user: OAuth2PasswordRequestForm=Depends(),db: Session = Depends(get_db)):

    user_details=db.query(model_database.UserDetails).filter(model_database.UserDetails.email==user.username).first()
    if not user_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with email: {user.username} does not exist")
    if not verify(user.password,user_details.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token=create_token(data={"user_id":user_details.id})
    return {"access_token":access_token,"token_type":"bearer"}
    


    