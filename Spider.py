# run "pip install -U requests[security]" to fix ssl error
# 多线程中
# s.config['keep_alive'] = False 关闭长链接

from init import import_blog, update_blog, start_download, start_load_all_image, start_load_new_image
from Works.KeyManager import check_key
from Config import spider_log


def main_menu():
    print("欢迎使用大橙喵爬虫,请选择功能")
    print("1.检查key")
    print("2.导入博客列表")
    print("3.刷新博客信息")
    print("4.爬取所有图片")
    print("5.爬取新发布图片")
    print("6.开始运行下载功能")
    print("其他.退出程序")
    selection = input()
    select_item(selection)


def select_item(selection):
    item = {
        "1": check_key,
        "2": import_blog,
        "3": update_blog,
        "4": start_load_all_image,
        "5": start_load_new_image,
        "6": start_download,
    }
    item.get(selection, exit)()
    spider_log.info("*" * 15 + " 执行完毕 " + "*" * 15)


if __name__ == '__main__':
    main_menu()
