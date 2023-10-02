from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer
Base = declarative_base()

class MatchUser(Base):
    __tablename__ = 'match_user'
    id = Column(Integer, primary_key=True, nullable=False)
    match_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)