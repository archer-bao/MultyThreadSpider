from datetime import datetime
from os import rename

from Config import spider_log
from DataControl.Repo import add_item
from DataControl.Repo import load_download_item
from Obj.Blog import Blog
from Obj.Image import Image
from Obj.Spider import Spider
from Obj.Video import Video
from Works.ResDownloader import ResDownloader
from Works.UpdateBlog import UpdateBlog
from time import sleep


def import_blog():
    spider_log.info("开始导入")
    with open(r"./blog_data.txt", "r", encoding="utf-8") as f:
        for line in f:
            if len(line) > 1:
                blog = Blog(url=line.replace("\n", ""))
                add_item(blog)

    new_file_name = "./import_finished{}.txt".format(datetime.now().strftime("%Y%m%d%H%M%S"))
    rename("./blog_data.txt", new_file_name)
    spider_log.info("导入完毕，旧文件被重命名为 {}".format(new_file_name))
    spider_log.info("开始更新博主信息")
    update_blog()


def update_blog():
    up = UpdateBlog()
    up.start()
    up.join()


def download_item(item_list):
    while len(item_list) > 0:
        d = None
        for i in range(8):
            try:
                item = item_list.pop(0)
                d = ResDownloader(item.id, item.__class__)
                d.start()
            except IndexError:
                d.join()
        d.join()
        sleep(5)


def download_image():
    spider_log.info("下载图片开始运行")
    item_list = load_download_item(Image)
    download_item(item_list)
    spider_log.info("下载图片结束")


def download_video():
    spider_log.info("下载视频开始运行")
    item_list = load_download_item(Video)
    download_item(item_list)
    spider_log.info("下载视频结束")


def load_all_image():
    s = Spider()
    s.load_all_image()
    s.start_()


def load_new_image():
    s = Spider()
    s.load_new_image()
    s.start_()


def load_all_video():
    s = Spider()
    s.load_all_video()
    s.start_()


def load_new_video():
    s = Spider()
    s.load_new_video()
    s.start_()
