from datetime import datetime
from queue import Queue
from threading import Thread

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from Config import spider_log
from DataControl.Key import get_newest_key
from DataControl.Repo import load_blog_list, reset_blog_loaded, load_download_item_and_blog_list
from Obj.Image import Image
from Works.FlushKey import FlushKey
from Works.LoadImage import LoadImage
from Works.ResDownloader import ResDownloader

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def thread_runner(work_queue, threads=4):
    timer = 0
    while not work_queue.empty():
        work = work_queue.get()
        work.start()
        timer += 1
        if timer % threads == 0:
            work.join()


def create_spider_work_queue():
    spider_log.info("开始创建工作队列")
    blog_list = load_blog_list()
    work_queue = Queue()
    for blog in blog_list:
        for offset in range(21):
            load_image = LoadImage(blog, offset=offset)
            work_queue.put(load_image)
    spider_log.info("创建工作队列完成")
    return work_queue


def check_key():
    spider_log.info("检查API key")
    key = get_newest_key()
    if (datetime.now() - key.UpdateTime).days > 7:
        spider_log.info("API Key已过期，现在开始刷新")
        f = FlushKey()
        f.start()
        f.join()
    spider_log.info("检查API key 结束")


def run_spider():
    spider_log.info("爬虫开始运行")
    check_key()
    work_queue = create_spider_work_queue()

    work_manager = Thread(target=thread_runner, args=(work_queue,))
    work_manager.start()
    work_manager.join()

    spider_log.info("本次爬取结束，开始清理工作")

    spider_log.info("开始重置Blog状态")
    reset_blog_loaded()
    spider_log.info("重置Blog状态完成")


def create_download_work_queue():
    spider_log.info("开始创建工作队列")
    item_list = load_download_item_and_blog_list(Image)
    work_queue = Queue()
    for item in item_list:
        d = ResDownloader(item.id, item.__class__)
        work_queue.put(d)
    spider_log.info("创建工作队列完成")
    return work_queue


def run_download():
    spider_log.info("下载开始运行")
    work_queue = create_download_work_queue()
    work_manager = Thread(target=thread_runner, args=(work_queue,))
    work_manager.start()
    work_manager.join()
    spider_log.info("下载结束")


if __name__ == '__main__':
    # while True:
    #     run_spider()
    #     run_download()
    #     spider_log.info("下次爬取将在3600s后执行")
    #     sleep(3600)

    run_download()
    # f = FlushKey()
    # f.start()
    # f.join()