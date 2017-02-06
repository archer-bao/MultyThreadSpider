import threading
import time
import logging


class Progress(threading.Thread):
    interval = 1
    total_size = 0
    finished_size = 0
    old_size = 0
    __stop = False

    def __init__(self, interval=0.5):
        self.interval = interval
        threading.Thread.__init__(self)

    def run(self):
        print('       Total       Finished      Percent        Speed')
        while not self.__stop:
            time.sleep(self.interval)
            if self.total_size > 0:
                percent = self.finished_size / self.total_size * 100
                speed = (self.finished_size - self.old_size) / self.interval
                msg = '%12d B %12d B %10.2f%% %12d B/s' % (self.total_size, self.finished_size, percent, speed)
                print(msg)

                self.old_size = self.finished_size
            else:
                logging.error('Total size is zero')

    def stop(self):
        self.__stop = True

    def update(self, finished_size, total_size):
        self.finished_size = finished_size
        self.total_size = total_size
