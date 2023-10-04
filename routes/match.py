import time
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

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# match crud
@router.get("/match")
def get_match_all(token: Annotated[str, Depends(oauth2_scheme)]):
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

@router.get("/match/{match_id}")
def get_match(match_id: int, token: Annotated[str, Depends(oauth2_scheme)]):
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

@router.post("/match")
def create_match(date: str, slot: int, token: Annotated[str, Depends(oauth2_scheme)]):
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
    