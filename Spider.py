from Works.KeyManager import check_key


# run "pip install -U requests[security]" to fix ssl error
# 加载key -》 检查key 是否有效-》 使用Key读取博客信息-》读取博客下的多媒体资源
# 多线程中
# s.config['keep_alive'] = False 关闭长链接


def show_menu():
    print("欢迎使用大橙喵爬虫,请选择功能")
    print("1.刷新key")
    print("2.导入博客列表")
    print("3.开始运行爬虫")
    print("4.退出程序")


def select_item(selection):
    item = {
        "1": check_key,
        "4": exit
    }
    item.get(selection, wrong_selection)()


def wrong_selection():
    print("输入错误，请重试")


if __name__ == '__main__':
    show_menu()
    selection = input()
    select_item(selection)
