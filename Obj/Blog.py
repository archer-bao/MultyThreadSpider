from Config import BaseModel
from sqlalchemy.types import *
from sqlalchemy import Column


class Blog(BaseModel):
    __tablename__ = "blog"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    url = Column(VARCHAR)
    name = Column(VARCHAR)
    alive = Column(Integer)
    loaded = Column(Integer)

    def __init__(self, url,  name, alive, loaded):
        self.url = url
        self.name = name
        self.alive = alive
        self.loaded = loaded


