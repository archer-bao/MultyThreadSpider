from Data.Database import Init


def start():
    init = Init()
    init.start()
    init.join()
    return init
