import time
from fastapi import FastAPI

#utils
from utils import send_mail

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


@app.get("/match")
def get_match_all():
    stmt = select(Match)
    with Session(engine) as session:
        result =  session.execute(stmt)
        details = []
        for row in result:
            details.append({"id": row[0].id, "date": row[0].date, "slot": row[0].slot})
        if details:
            response = {}
            response["status"] = "ok"
            response["message"] = "Match found"
            response["details"] = details
            return response
        else:
            response = {}
            response["status"] = "error"
            response["message"] = "No matche found"
            return response


@app.get("/match/{match_id}")
def get_match(match_id: int):
    stmt = select(Match).where(Match.id == match_id)
    with Session(engine) as session:
        result =  session.execute(stmt).first()
        if result:
            response = {}
            response["status"] = "ok"
            response["message"] = "Match found"
            response["details"] = {"id": result[0].id, "date": result[0].date, "slot": result[0].slot}
            return response
        else:
            response = {}
            response["status"] = "error"
            response["message"] = "Match not found"
            return response

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
    send_mail = False
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