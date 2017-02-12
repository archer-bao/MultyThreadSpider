import http.client
from os import rename, remove
from os.path import exists, getsize
from urllib.parse import urlparse
from  http.client import RemoteDisconnected
from time import sleep

from Config import spider_log as logging


class Downloader(object):
    '''''文件下载器'''
    url = ''
    file_path = ''
    temp_file_path = ''
    total_size = 0
    connection = None
    finished_size = 0

    def __init__(self, full_url_str, file_path):
        '''''初始化'''
        self.url = urlparse(full_url_str.replace("https", "http"))
        self.file_path = file_path

    def check_temp_file(self):
        if exists(self.temp_file_path):
            if getsize(self.temp_file_path) == self.total_size:
                self.temp_file_rename()
                logging.info("{}下载完成！".format(self.url))
                return
            else:
                remove(self.temp_file_path)
                logging.info("临时文件不完整,已删除")

    def make_request(self):
        if self.url.scheme == 'https':
            self.connection = http.client.HTTPSConnection(self.url.netloc)
        else:
            self.connection = http.client.HTTPConnection(self.url.netloc)
        self.connection.request('GET', self.url.path)
        response = self.connection.getresponse()
        return response

    def temp_file_rename(self):
        logging.info("临时文件已下载完成{}".format(self.temp_file_path))
        rename(self.temp_file_path, self.file_path)
        logging.info("临时文件已改名{}".format(self.file_path))

    def save_file(self, response):
        file = open(self.temp_file_path, 'wb')
        if file:
            while not response.closed:
                buffers = response.read(1024)
                file.write(buffers)
                self.finished_size += len(buffers)
                if self.finished_size >= self.total_size:
                    break
            file.close()
            self.temp_file_rename()
        else:
            logging.error('Create local file {} failed'.format(self.file_path))

    def download(self):
        '''''执行下载，返回True或False'''
        if self.url == '' or self.url == None or self.file_path == '' or self.file_path == None:
            logging.error('Invalid parameter for Downloader')
            return False
        self.temp_file_path = self.file_path + "_temp"
        logging.info("开始下载:{} 保存路径：{}".format(self.url, self.temp_file_path))
        try:
            response = self.make_request()
        except RemoteDisconnected:
            logging.info("请求被限制,等待重试")
            sleep(5)
            logging.info("请求重试")
            response = self.make_request()
        if response.status == 200:
            t_size = response.getheader('Content-Length')
            self.total_size = int(t_size)
            self.check_temp_file()
            if self.total_size > 0:
                self.save_file(response)
            else:
                logging.error('Request file {} size failed'.format(self.file_path))
        else:
            logging.error('HTTP/HTTPS request failed, status code:{}'.format(response.status))
        self.connection.close()
        logging.info("{} 下载完成！".format(self.url))
        return True
