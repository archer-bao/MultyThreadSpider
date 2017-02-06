from Config import session
from Obj.Key import Key
from random import seed, randint
from time import time
from sqlalchemy import func


def get_key():
    seed(time())
    count = session.query(func.count('*')).select_from(Key).scalar()
    id = randint(1, count)
    return session.query(Key).get(id)


def get_all_key():
    l = session.query(Key).all()
    return l


def update_key_use(func):
    def wrapper(*args, **kwargs):
        k = session.query(Key).with_lockmode('update').get(args[0].key.id)
        k.UseTimes += 1
        session.commit()
        # session.remove()
        return func(*args, **kwargs)

    return wrapper


def commit():
    session.commit()
