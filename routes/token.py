from typing import Annotated
import hashlib
#fastapi
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
#db
from db_connection import engine
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
#schemas
from schemas.user import User
#utils
from utils.token import create_token

router = APIRouter()

# auth
@router.post("/token")
def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]): 
    username = form_data.username
    password = form_data.password
    password_md5 = hashlib.md5(password.encode()).hexdigest()
    stmt = select(User).where(User.username == username, User.password == password_md5)
    with Session(engine) as session:
        result =  session.execute(stmt).first()
        if result is not None:
            token = create_token(result[0].id)
            return {"access_token": token, "token_type": "bearer"}
        else:
            response = {}
            response["status"] = "error"
            response["message"] = "User not authenticated"
            return response
