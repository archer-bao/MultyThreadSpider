import hashlib
from os import makedirs
from os.path import join, basename
from threading import Thread

from DataControl.Repo import get_item, get_item_blog, update_item_path
from Config import resource_folder, session
from Downloader.Downloader import Downloader


class ResDownloader(Thread):
    item = None
    blog = None

    def __init__(self, item_id, item_class):
        super(ResDownloader, self).__init__()
        self.item = get_item(item_class, item_id)
        self.blog = get_item_blog(self.item)

    def run(self):
        folder_path = folder_path_builder(self.blog, "images")
        file_path = file_path_builder(self.item.url, folder_path)
        down = Downloader(self.item.url, file_path)
        try:
            down.download()
        except FileNotFoundError:
            makedirs(folder_path)
            down.download()
        update_item_path(item=self.item, item_class=self.item.__class__, path=file_path)
        session.remove()


def file_path_builder(url, folder_path):
    output_file_path = join(folder_path, basename(url))
    return output_file_path


def folder_path_builder(blog, folder):
    # 基准目录+博客MD5+images
    # exam:/root/output/ASDHSADHUWNK12334324QWEQW/images
    encoded_blog_name = encode_blog_name(blog)
    return join(resource_folder, encoded_blog_name, folder)


def encode_blog_name(blog):
    return encrypt_md5(blog.name)


def encrypt_md5(src):
    m2 = hashlib.md5()
    m2.update(bytes(src, encoding="utf8"))
    return m2.hexdigest().upper()
