import time
from fastapi import FastAPI

#connection to database
from db_connection import engine, db_connection
from sqlalchemy import select, insert
from sqlalchemy.orm import Session

#schemas
from schemas.match import Match
from schemas.user import User
from schemas.match_user import MatchUser

# http server
app = FastAPI()


@app.get("/match/{match_id}")
def get_match(match_id: int):
    stmt = select(Match).where(Match.id == match_id)
    with Session(engine) as session:
        for row in session.execute(stmt):
            return row[0]


@app.post("/match")
def create_match(date: str, slot: int):
    #check if input is valid
    if slot < 9 or slot > 23:
        response = {}
        response["status"] = "error"
        response["message"] = "Invalid slot"
        return response
    try:
        date_date = time.strptime(date, '%Y-%m-%d')
    except ValueError:
        response = {}
        response["status"] = "error"
        response["message"] = "Invalid date"
        return response
    #check if match already exists
    stmt = select(Match).where(Match.date == date, Match.slot == slot)
    with Session(engine) as session:
        result =  session.execute(stmt).first()
        print(result)
        if result is not None:
            response = {}
            response["status"] = "error"
            response["message"] = "Match already exists"
            return response
    #then create match
    stmt = insert(Match).values(date=date, slot=slot)
    with Session(engine) as session:
        session.execute(stmt)
        session.commit()
        response = {}
        response["status"] = "ok"
        response["message"] = "Match created"
        return response

    
@app.post("/book_user")
def create_match_user(date: str, slot: int, user_id: int):
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
        return response