from sqlalchemy.types import *
from sqlalchemy import Column
from Config import BaseModel
from datetime import datetime


class Image(BaseModel):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    url = Column(VARCHAR)
    blog_id = Column(Integer)
    path = Column(VARCHAR)
    add_time = Column(DateTime)
    release_time = Column(DateTime)

    def __init__(self, url, blog_id, release_time):
        self.url = url
        self.blog_id = blog_id
        self.add_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.release_time = release_time
