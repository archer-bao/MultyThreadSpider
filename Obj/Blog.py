from Config import BaseModel
from sqlalchemy.types import *
from sqlalchemy import Column


class Blog(BaseModel):
    __tablename__ = "blog"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    url = Column(VARCHAR)
    title = Column(VARCHAR)
    name = Column(VARCHAR)
    alive = Column(Integer)
    loaded = Column(Integer)
