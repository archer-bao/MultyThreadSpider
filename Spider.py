# run "pip install -U requests[security]" to fix ssl error
# 多线程中
# s.config['keep_alive'] = False 关闭长链接
from datetime import datetime
from os import rename
from queue import Queue

from Config import spider_log
from DataControl.Repo import add_item
from DataControl.Repo import load_blog_list
from Obj.Blog import Blog
from Works.KeyManager import check_key
from Works.LoadImage import LoadImage
from Works.UpdateBlog import UpdateBlog


def show_menu():
    print("欢迎使用大橙喵爬虫,请选择功能")
    print("1.检查key")
    print("2.导入博客列表")
    print("3.刷新博客信息")
    print("4.开始运行图片爬虫")
    print("其他.退出程序")


def select_item(selection):
    item = {
        "1": check_key,
        "2": import_blog,
        "3": update_blog,
        "4": start_spider,
    }
    item.get(selection, exit)()


def start_spider():
    works = create_spider_work_queue()
    work = None
    while not works.empty():
        for i in range(16):
            work = works.get()
            work.start()
        work.join()


def update_blog():
    up = UpdateBlog()
    up.start()
    up.join()


def import_blog():
    spider_log.info("开始导入")
    with open(r"./blog_data.txt", "r", encoding="utf-8") as f:
        for line in f:
            if len(line) > 1:
                blog = Blog(url=line.replace("\n", ""), name="", alive=1, loaded=0)
                add_item(blog)

    new_file_name = "./import_finished{}.txt".format(datetime.now().strftime("%Y%m%d%H%M%S"))
    rename("./blog_data.txt", new_file_name)
    spider_log.info("导入完毕，旧文件被重命名为 {}".format(new_file_name))
    spider_log.info("开始更新博主信息")
    update_blog()


def create_spider_work_queue():
    spider_log.info("开始创建工作队列")
    blog_id_list = load_blog_list()
    work_queue = Queue()
    for blog_id in blog_id_list:
        for offset in range(40):
            load_image = LoadImage(blog_id, offset=offset)
            work_queue.put(load_image)
    spider_log.info("创建工作队列完成")
    return work_queue


if __name__ == '__main__':
    show_menu()
    selection = input()
    select_item(selection)
