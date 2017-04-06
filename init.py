from datetime import datetime
from os import rename

from Config import spider_log
from DataControl.Repo import add_item
from DataControl.Repo import load_download_item
from Obj.Blog import Blog
from Obj.Image import Image
from Obj.Spider import Spider
from Works.ResDownloader import ResDownloader
from Works.UpdateBlog import UpdateBlog


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


def start_download():
    spider_log.info("下载开始运行")
    item_list = load_download_item(Image)
    while len(item_list) > 0:
        d = None
        for i in range(16):
            try:
                item = item_list.pop(0)
                d = ResDownloader(item.id, item.__class__)
                d.start()
            except IndexError:
                d.join()
        d.join()

    spider_log.info("下载结束")


def start_load_all_image():
    s = Spider()
    s.load_all_image()
    s.start_()


def start_load_new_image():
    s = Spider()
    s.load_new_image()
    s.start_()
