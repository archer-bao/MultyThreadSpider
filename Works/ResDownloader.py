from os import makedirs
from os.path import basename, exists
from os.path import join
from subprocess import call
from threading import Thread

from Config import resource_folder, session
from Config import spider_log
from DataControl.Repo import get_item, get_item_blog
from Obj.Image import Image


class ResDownloader(Thread):
    item = None
    blog = None
    item_id = None
    item_class = None

    def __init__(self, item_id, item_class):
        super(ResDownloader, self).__init__()
        self.item_id = item_id
        self.item_class = item_class

    def run(self):
        self.item = get_item(self.item_class, self.item_id)
        self.blog = get_item_blog(self.item)
        folder_path = get_file_folder_path(self.blog, "images" if self.item_class is Image else "videos")
        file_path = get_file_path(self.item.url, folder_path)
        # eg.  wget https://vtt.tumblr.com/tumblr_o6cjopNCcN1vt349a.mp4 -O /mnt/storage/tumblr_o6cjopNCcN1vt349a.mp4
        # cmd = "wget -c {} -O {}".format(self.item.url, file_path)
        cmd = ["wget", "-cq", self.item.url.replace("https", "http"), "-O", file_path]
        spider_log.info("下载 Id:{} 命令:{}".format(self.item.id, cmd))
        p = call(cmd)
        success = p is 0
        spider_log.info("Id:{} 结果为 {}".format(self.item.id, str(success)))
        if success:
            self.success_callback(file_path)
        else:
            self.fail_callback()
        session.remove()

    def success_callback(self, file_path):
        self.item.file_path = file_path
        session.commit()

    def fail_callback(self):
        self.item.file_path = "#error"
        session.commit()


def get_file_path(url, folder_path):
    output_file_path = join(folder_path, basename(url))
    return output_file_path


def get_file_folder_path(blog, folder):
    # 基准目录+博客name+images
    # example:/root/output/ASDHSADHUWNK12334324QWEQW/images
    path = join(resource_folder, blog.name, folder)
    if not exists(path):
        makedirs(path)
    return path
