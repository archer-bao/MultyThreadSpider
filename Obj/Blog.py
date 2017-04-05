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
    posts = Column(Integer)

    def __init__(self, url):
        self.url = url
        self.name = None
        self.posts = 0
        self.alive = 1
        self.loaded = 0
