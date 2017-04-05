from math import ceil

from Config import spider_log
from DataControl.Repo import load_alive_blog_list
from Works.LoadImage import LoadImage


class Spider:
    def __init__(self):
        self.work_queue = []

    def create_spider_work_queue(self):
        spider_log.info("开始创建工作队列")
        blog_id_list = load_alive_blog_list()
        for blog in blog_id_list:
            # block = offset * 20
            start_block = blog.loaded
            end_block = int(ceil(blog.posts / 20))
            # print("blogId:{} start:{} end:{}".format(blog.id, start_block, end_block))

            for block in range(start_block, end_block):
                load_image = LoadImage(blog.id, offset=block * 20)
                self.work_queue.append(load_image)
        spider_log.info("创建工作队列完成")

    def start_spider(self):
        works = self.work_queue
        work = None
        while len(self.work_queue) > 0:
            for i in range(16):
                try:
                    work = works.pop(0)
                    work.start()
                except IndexError:
                    work.join()
                    return
            work.join()
