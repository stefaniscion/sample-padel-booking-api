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
        return {"message": "Invalid slot"}
    try:
        date_date = time.strptime(date, '%Y-%m-%d')
    except ValueError:
        return {"message": "Invalid date"}
    #check if match already exists
    stmt = select(Match).where(Match.date == date, Match.slot == slot)
    with Session(engine) as session:
        result =  session.execute(stmt).first()
        print(result)
        if result is not None:
            return {"message": "Match already exists"}
    #then create match
    stmt = insert(Match).values(date=date, slot=slot)
    with Session(engine) as session:
        session.execute(stmt)
        session.commit()
        return {"message": "Match created"}

    
#@app.get("/book_match/{match_id}/{user_id}/{slot_id}")
#def book_match(match_id:int, user_id: int, slot_id: int):
#    pass
#     