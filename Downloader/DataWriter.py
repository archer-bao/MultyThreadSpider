import threading
from queue import Queue


class DataWriter(threading.Thread):
    filename = ''
    queue = Queue(128)
    data_dict = {'offset': 0, 'buffers_byte': b''}
    __stop = False

    def __init__(self, filename):
        self.filename = filename
        threading.Thread.__init__(self)

    def run(self):
        while not self.__stop:
            self.queue.get(True, 1)

    def put_data(self, data_dict):
        '''''将data_dict的数据放入队列，data_dict是一个字典，有两个元素：offset是偏移量，buffers_byte是二进制字节串'''
        self.queue.put(data_dict)

    def stop(self):
        self.__stop = True
