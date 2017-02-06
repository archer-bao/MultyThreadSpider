from sqlalchemy.types import *
from sqlalchemy import Column
from Config import BaseModel


class Image(BaseModel):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    url = Column(VARCHAR)
    blog_id = Column(Integer)
    path = Column(VARCHAR)
    add_time = Column(DateTime)
    release_time = Column(DateTime)
