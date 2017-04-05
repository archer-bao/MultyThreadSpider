# run "pip install -U requests[security]" to fix ssl error
# 多线程中
# s.config['keep_alive'] = False 关闭长链接

from MyUtils import import_blog, update_blog, start_download, start_spider
from Works.KeyManager import check_key
from Config import spider_log


def main_menu():
    while True:
        print("欢迎使用大橙喵爬虫,请选择功能")
        print("1.检查key")
        print("2.导入博客列表")
        print("3.刷新博客信息")
        print("4.开始运行图片爬虫")
        print("5.开始运行下载功能")
        print("9.自定义功能队列")
        print("其他.退出程序")
        selection = input()
        select_item(selection)


def select_item(selection):
    item = {
        "1": check_key,
        "2": import_blog,
        "3": update_blog,
        "4": start_spider,
        "5": start_download,
        "9": diy_combine,
    }
    item.get(selection, exit)()
    spider_log.info("*" * 15 + " 执行完毕 " + "*" * 15)


def diy_combine():
    print("请输入自定义功能组合，以','分割")
    print("Example: 1,2,3")
    combine = input()
    ops = combine.split(",")
    for op in ops:
        select_item(op)
    exit()


if __name__ == '__main__':
    main_menu()
