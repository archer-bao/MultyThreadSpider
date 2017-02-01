from Config import log
from Data.Resource import blog_queue, key_queue
from Services.SpiderService import load_image, load_video
from threading import Thread
from time import sleep

log.info("爬虫开始运行")
while True:
    while not blog_queue.empty():
        blog = blog_queue.get()
        while not key_queue.empty():
            for outer_offset in range(6):
                for inner_offset in range(5):
                    offset = outer_offset + inner_offset * 5
                    key = key_queue.get()
                    t1 = Thread(target=load_image, kwargs=dict(apikey=key, blog=blog, offset=offset))
                    t2 = Thread(target=load_video, kwargs=dict(apikey=key, blog=blog, offset=offset))
                    t1.start()
                    t2.start()
                    t1.join()
                    t2.join()
    sleep(3600)
