from DAOs.KeyDao import update_key_use_times


def use_key(func):
    def wrapper(*args, **kwargs):
        key = kwargs.get("apikey")
        update_key_use_times(key)
        return func(*args, **kwargs)

    return wrapper
