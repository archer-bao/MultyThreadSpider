from Config import log
from Data.Resource import blog_queue, key_queue
from Services.SpiderService import load_image, load_video
from threading import Thread
from time import sleep
from SpiderException.SpiderException import SpiderException
from queue import Queue

log.info("爬虫开始运行")
fail_queue = Queue()
while True:
    if not fail_queue.empty():
        inner_blog_queue = fail_queue
    else:
        inner_blog_queue = blog_queue
        while not inner_blog_queue.empty():
            blog = inner_blog_queue.get()
            while not key_queue.empty():
                key = key_queue.get()
                for outer_offset in range(4):
                    for inner_offset in range(6):
                        offset = outer_offset * 6 + inner_offset
                        if offset > 20:
                            break
                        try:
                            t1 = Thread(target=load_image, kwargs=dict(apikey=key, blog=blog, offset=offset))
                            t2 = Thread(target=load_video, kwargs=dict(apikey=key, blog=blog, offset=offset))
                            t1.start()
                            t2.start()
                            t1.join()
                            t2.join()
                        except SpiderException:
                            fail_queue.put(blog)
    sleep(3600)
