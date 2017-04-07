from init import import_blog, update_blog, download_image, load_all_image, load_new_image, \
    load_all_video, load_new_video, download_video
from Works.KeyManager import check_key
from Config import spider_log


def main_menu():
    menu = """欢迎使用大橙喵爬虫,请选择功能
1.检查key
2.导入博客列表
3.刷新博客信息
4.爬取所有图片
5.爬取新发布图片
6.爬取所有视频
7.爬取新发布视频
8.运行下载图片
9.运行下载视频
其他.退出程序"""
    print(menu)
    selection = input()
    select_item(selection)


def select_item(selection):
    item = {
        "1": check_key,
        "2": import_blog,
        "3": update_blog,
        "4": load_all_image,
        "5": load_new_image,
        "6": load_all_video,
        "7": load_new_video,
        "8": download_image,
        "9": download_video,
    }
    item.get(selection, exit)()
    spider_log.info("*" * 15 + " 执行完毕 " + "*" * 15)


if __name__ == '__main__':
    main_menu()
