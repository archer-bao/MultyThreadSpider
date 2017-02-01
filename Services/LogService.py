from DAOs.KeyDao import update_key_use_times
from threading import Thread


def use_key(func):
    def wrapper(*args, **kwargs):
        key = kwargs.get("apikey")
        t = Thread(target=update_key_use_times, args=(key,))
        t.daemon = True
        t.start()
        return func(*args, **kwargs)

    return wrapper
