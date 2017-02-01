from concurrent.futures import ThreadPoolExecutor

import time


def wait_on_b():
    time.sleep(5)
    return 5


def wait_on_a():
    time.sleep(5)
    return 6


executor = ThreadPoolExecutor(max_workers=2)
a = executor.submit(wait_on_b)
b = executor.submit(wait_on_a)
print(a.result())
print(b.result())
