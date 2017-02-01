from queue import Queue
from threading import Thread
from DAOs.BlogDao import get_blog_list
from DAOs.KeyDao import get_key_list


def to_queue(items, queue):
    for item in items:
        queue.put(item)


blog_queue = Queue()
key_queue = Queue()
to_queue(get_blog_list(), blog_queue)
to_queue(get_key_list(), key_queue)


class Init(Thread):
    def __init__(self):
        super(Init, self).__init__()

    def run(self):
        global blog_queue, key_queue
        to_queue(get_blog_list(), blog_queue)
        to_queue(get_key_list(), key_queue)
