from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String, DateTime
from Config import SQLALCHEMY_DATABASE_URI
from threading import Thread

# ===========数据库===========
DATABASE = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
DATABASE_SESSION = sessionmaker(bind=DATABASE)()
DATABASE_BASE = declarative_base()
DATABASE.Model = DATABASE_BASE
DATABASE.Column = Column
DATABASE.Integer = Integer
DATABASE.String = String
DATABASE.DateTime = DateTime


class Init(Thread):
    def __init__(self):
        super(Init, self).__init__()

    def run(self):
        global DATABASE, DATABASE_SESSION, DATABASE_BASE
        DATABASE = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
        DATABASE_SESSION = sessionmaker(bind=DATABASE)()
        DATABASE_BASE = declarative_base()
        DATABASE.Model = DATABASE_BASE
        DATABASE.Column = Column
        DATABASE.Integer = Integer
        DATABASE.String = String
        DATABASE.DateTime = DateTime
