import http.client
import logging
from urllib.parse import urlparse
from Downloader.Progress import Progress


class Downloader(object):
    '''''文件下载器'''
    url = ''
    filename = ''

    def __init__(self, full_url_str, filename):
        '''''初始化'''
        self.url = urlparse(full_url_str)
        self.filename = filename

    def download(self):
        '''''执行下载，返回True或False'''
        if self.url == '' or self.url == None or self.filename == '' or self.filename == None:
            logging.error('Invalid parameter for Downloader')
            return False
        print("开始下载:{} 保存路径：{}".format(self.url, self.filename))
        successed = False
        conn = None
        if self.url.scheme == 'https':
            conn = http.client.HTTPSConnection(self.url.netloc)
        else:
            conn = http.client.HTTPConnection(self.url.netloc)
        conn.request('GET', self.url.path)
        response = conn.getresponse()
        if response.status == 200:
            total_size = response.getheader('Content-Length')
            total_size = (int)(total_size)
            if total_size > 0:
                finished_size = 0
                file = open(self.filename, 'wb')
                if file:
                    progress = Progress()
                    progress.start()
                    while not response.closed:
                        buffers = response.read(1024)
                        file.write(buffers)

                        finished_size += len(buffers)
                        progress.update(finished_size, total_size)
                        if finished_size >= total_size:
                            break
                            # ... end while statment
                    file.close()
                    progress.stop()
                    progress.join()
                else:
                    logging.error('Create local file %s failed' % (self.filename))
                    # ... end if statment
            else:
                logging.error('Request file %s size failed' % (self.filename))
                # ... end if statment
        else:
            logging.error('HTTP/HTTPS request failed, status code:%d' % (response.status))
            # ... end if statment
        conn.close()
        print("下载完成！")
        return successed
        # ... end download() method
