from random import seed, randint
from time import time

from sqlalchemy import func

from Config import session
from Obj.Key import Key


def get_key():
    seed(time())
    count = session.query(func.count('*')).select_from(Key).scalar()
    id = randint(1, count)
    return session.query(Key).get(id)


def get_all_key():
    return session.query(Key).all()


def get_newest_key():
    return session.query(Key).order_by(Key.UpdateTime.desc()).first()


def update_key_use(key):
    def decorate(func):
        def wrapper(*args, **kwargs):
            k = session.query(Key).with_lockmode('update').get(key.id)
            k.UseTimes += 1
            session.commit()
            return func(*args, **kwargs)

        return wrapper

    return decorate


def commit():
    session.commit()
