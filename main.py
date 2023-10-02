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


