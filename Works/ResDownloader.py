from os.path import join, basename
from threading import Thread

from Config import resource_folder, session
from DataControl.Repo import get_item, get_item_blog
from Downloader.Downloader import Downloader
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
        folder_path = folder_path_builder(self.blog, "images" if self.item_class is Image else "videos")
        file_path = file_path_builder(self.item.url, folder_path)
        down = Downloader(self.item.url, file_path)
        success = down.download()
        if success:
            self.update_item(file_path)
        else:
            session.delete(self.item)
            session.commit()
        session.remove()

    def update_item(self, file_path):
        self.item.file_path = file_path
        session.commit()


def file_path_builder(url, folder_path):
    output_file_path = join(folder_path, basename(url))
    return output_file_path


def folder_path_builder(blog, folder):
    # 基准目录+博客name+images
    # example:/root/output/ASDHSADHUWNK12334324QWEQW/images
    return join(resource_folder, blog.name, folder)
