from Config import session
from Obj.Key import Key


def get_key():
    return session.query(Key).order_by(Key.UseTimes.asc()).first()


def get_all_key():
    l = session.query(Key).all()
    return l


def update_key_use(func):
    def wrapper(*args, **kwargs):
        k = session.query(Key).with_lockmode('update').get(args[0].key.id)
        k.UseTimes += 1
        session.commit()
        return func(*args, **kwargs)

    return wrapper



def commit():
    session.commit()
