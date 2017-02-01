from Init import SPIDER_DATABASE_SESSION
from Objects.Key import Key
from sqlalchemy import asc, desc
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from Config import SQLALCHEMY_DATABASE_URI


def get_key_list():
    return SPIDER_DATABASE_SESSION.query(Key).order_by(asc(Key.UseTimes)).all()


def get_oldest_key():
    return SPIDER_DATABASE_SESSION.query(Key).order_by(desc(Key.UpdateTime)).first()


def update_key_use_times(key):
    session = init_ession()
    session.query(Key).filter(Key.id == key.id).update({
        Key.UseTimes: Key.UseTimes + 1
    })
    SPIDER_DATABASE_SESSION.commit()


def init_ession():
    SPIDER_DATABASE = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
    SPIDER_DATABASE_SESSION = sessionmaker(bind=SPIDER_DATABASE)()
    return SPIDER_DATABASE_SESSION
