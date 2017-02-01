from Data.Database import DATABASE_SESSION
from Objects.Key import Key
from sqlalchemy import asc, desc


def get_key_list():
    return DATABASE_SESSION.query(Key).order_by(asc(Key.UseTimes)).all()


def get_oldest_key():
    return DATABASE_SESSION.query(Key).order_by(desc(Key.UpdateTime)).first()


def update_key_use_times(key):

    DATABASE_SESSION.query(Key).filter(Key.id == key.id).update({
        Key.UseTimes: Key.UseTimes + 1
    })
    DATABASE_SESSION.commit()


