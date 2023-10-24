from typing import Annotated
#fastapi
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
#db
from db_connection import engine
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
#schemas
from schemas.match import Match
from schemas.user import User
from schemas.match_user import MatchUser
#utils
from utils.mail import send_mail
from utils.token import get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# book routes   
@router.post("/book_user")
def create_match_user(date: str, slot: int, user_id: int, token: Annotated[str, Depends(oauth2_scheme)]):
    '''book specified user in a existing match'''
    match_full = False
    #check if user exists
    stmt = select(User).where(User.id == user_id)
    with Session(engine) as session:
        result =  session.execute(stmt).first()
        if result is None:
            response = {}
            response["status"] = "error"
            response["message"] = "User not exists"
            return response
    #check if match exists
    stmt = select(Match).where(Match.date == date, Match.slot == slot)
    with Session(engine) as session:
        result =  session.execute(stmt).first()
        print(result)
        if result is None:
            response = {}
            response["status"] = "error"
            response["message"] = "Match not exists"
            return response
        else:
            match_id = result[0].id
    #check if here is space (max 4 users)
    stmt = select(MatchUser).where(MatchUser.match_id == match_id)
    with Session(engine) as session:
        result =  session.execute(stmt).all()
        if len(result) >= 4:
            response = {}
            response["status"] = "error"
            response["message"] = "Match is full"
            return response
        if len(result) == 3:
            match_full = True
    #check if user already booked this match
    stmt = select(MatchUser).where(MatchUser.match_id == match_id, MatchUser.user_id == user_id)
    with Session(engine) as session:
        result =  session.execute(stmt).first()
        if result is not None:
            response = {}
            response["status"] = "error"
            response["message"] = "User already booked match"
            return response
    #then create match_user
    stmt = insert(MatchUser).values(match_id=match_id, user_id=user_id)
    with Session(engine) as session:
        session.execute(stmt)
        session.commit()
        response = {}
        response["status"] = "ok"
        response["message"] = "User booked match"
        response["details"] = {"date": date, "slot": slot}
        if match_full:
            #obtain emails of all users
            stmt = select(User).where(User.id == user_id)
            with Session(engine) as session:
                result =  session.execute(stmt).all()
                emails = []
                for row in result:
                    emails.append(row[0].email)
            for email in emails:
                send_mail("Match successfully booked", "This email is to inform you that the match you booked is now full. Have fun!", email)
        return response
    
@router.post("/book_me")
def create_match_user_me(date: str, slot: int, token: Annotated[str, Depends(oauth2_scheme)]):
    '''book authenticated user in a existing match'''
    user_id = get_current_user(token)
    if user_id is None:
        response = {}
        response["status"] = "error"
        response["message"] = "User not authenticated"
        return response
    match_full = False
    #check if user exists
    stmt = select(User).where(User.id == user_id)
    with Session(engine) as session:
        result =  session.execute(stmt).first()
        if result is None:
            response = {}
            response["status"] = "error"
            response["message"] = "User not exists"
            return response
    #check if match exists
    stmt = select(Match).where(Match.date == date, Match.slot == slot)
    with Session(engine) as session:
        result =  session.execute(stmt).first()
        print(result)
        if result is None:
            response = {}
            response["status"] = "error"
            response["message"] = "Match not exists"
            return response
        else:
            match_id = result[0].id
    #check if here is space (max 4 users)
    stmt = select(MatchUser).where(MatchUser.match_id == match_id)
    with Session(engine) as session:
        result =  session.execute(stmt).all()
        if len(result) >= 4:
            response = {}
            response["status"] = "error"
            response["message"] = "Match is full"
            return response
        if len(result) == 3:
            match_full = True
    #check if user already booked this match
    stmt = select(MatchUser).where(MatchUser.match_id == match_id, MatchUser.user_id == user_id)
    with Session(engine) as session:
        result =  session.execute(stmt).first()
        if result is not None:
            response = {}
            response["status"] = "error"
            response["message"] = "User already booked match"
            return response
    #then create match_user
    stmt = insert(MatchUser).values(match_id=match_id, user_id=user_id)
    with Session(engine) as session:
        session.execute(stmt)
        session.commit()
        response = {}
        response["status"] = "ok"
        response["message"] = "User booked match"
        response["details"] = {"date": date, "slot": slot}
        match_full = True
        if match_full:
            #obtain emails of all users
            stmt = select(User).where(User.id == user_id)
            with Session(engine) as session:
                result =  session.execute(stmt).all()
                emails = []
                for row in result:
                    emails.append(row[0].email)
            for email in emails:
                send_mail("Match successfully booked", "This email is to inform you that the match you booked is now full. Have fun!", email)
        return response