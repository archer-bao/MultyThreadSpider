import hashlib
from os.path import join, basename
from threading import Thread

from Config import resource_folder, session
from DataControl.Repo import get_item, get_item_blog
from Downloader.Downloader import Downloader


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
        folder_path = folder_path_builder(self.blog, "images")
        file_path = file_path_builder(self.item.url, folder_path)
        down = Downloader(self.item.url, file_path)
        success = down.download()
        if success:
            self.update_item(file_path)
        session.remove()

    def update_item(self, file_path):
        self.item.path = file_path
        session.commit()


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
