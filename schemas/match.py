from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Date
Base = declarative_base()

class Match(Base):
    __tablename__ = 'match'
    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(Date(), nullable=False)
    slot = Column(Integer, nullable=False)