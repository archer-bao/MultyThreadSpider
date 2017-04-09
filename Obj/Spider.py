from math import ceil

from Config import spider_log
from DataControl.Repo import load_alive_blog_list
from Works.LoadImage import LoadImage
from Works.LoadVideo import LoadVideo


class Spider:
    def __init__(self):
        self.work_queue = []

    def start_(self):
        works = self.work_queue
        work = None
        while len(self.work_queue) > 0:
            for i in range(8):
                try:
                    work = works.pop(0)
                    work.start()
                except IndexError:
                    work.join()
                    return
            work.join()

    def load_all_image(self):
        spider_log.info("开始执行爬取所有图片")
        blog_id_list = load_alive_blog_list()
        for blog in blog_id_list:
            start_block = blog.loaded_image
            end_block = int(ceil(blog.posts / 20))
            self._load_image(blog, start_block, end_block)
        spider_log.info("爬取所有图片完成")

    def load_new_image(self):
        spider_log.info("开始执行爬取新图片")
        blog_id_list = load_alive_blog_list()
        for blog in blog_id_list:
            start_block = 0
            end_block = int(ceil(blog.posts / 20 - blog.loaded_image))
            self._load_image(blog, start_block, end_block)
        spider_log.info("爬取新图片完成")

    def _load_image(self, blog, start_block, end_block):
        for block in range(start_block, end_block):
            load_image = LoadImage(blog.id, offset=block * 20)
            self.work_queue.append(load_image)

    def load_all_video(self):
        spider_log.info("开始执行爬取所有视频")
        blog_id_list = load_alive_blog_list()
        for blog in blog_id_list:
            start_block = blog.loaded_video
            end_block = int(ceil(blog.posts / 20))
            self._load_video(blog, start_block, end_block)
        spider_log.info("爬取所有视频完成")

    def load_new_video(self):
        spider_log.info("开始执行爬取新视频")
        blog_id_list = load_alive_blog_list()
        for blog in blog_id_list:
            start_block = 0
            end_block = int(ceil(blog.posts / 20 - blog.loaded_video))
            self._load_video(blog, start_block, end_block)
        spider_log.info("爬取新视频完成")

    def _load_video(self, blog, start_block, end_block):
        for block in range(start_block, end_block):
            load_video = LoadVideo(blog.id, offset=block * 20)
            self.work_queue.append(load_video)
