from threading import Thread
from os.path import join, basename


class Download(Thread):
    def __init__(self, item, blog):
        super(Download, self).__init__()

    def run(self):
        pass


def filename_builder(url, save_folder):
    output_file_path = join(save_folder, basename(url))
    return output_file_path
