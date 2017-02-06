from sqlalchemy.types import *
from sqlalchemy import Column
from Config import BaseModel


class Key(BaseModel):
    __tablename__ = "key"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    ConsumerKey = Column(VARCHAR)
    ConsumerSecret = Column(VARCHAR)
    Token = Column(VARCHAR)
    TokenSecret = Column(VARCHAR)
    UpdateTime = Column(DateTime)
    UseTimes = Column(Integer)
