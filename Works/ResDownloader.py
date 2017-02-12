from threading import Thread
from os.path import join, basename
from os import makedirs
from Config import resource_folder
import hashlib
from Downloader.Downloader import Downloader
from Config import session


class ResDownloader(Thread):
    def __init__(self, item, blog):
        super(ResDownloader, self).__init__()
        self.item = item
        self.blog = blog

    def run(self):
        folder_path = folder_path_builder(self.blog, "images")
        file_path = file_path_builder(self.item.url, folder_path)
        down = Downloader(self.item.url, file_path)
        try:
            down.download()
        except FileNotFoundError:
            makedirs(folder_path)
            down.download()
        self.item.path = file_path
        session.commit()
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
