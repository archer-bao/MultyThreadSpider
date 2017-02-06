from Works.LoadImage import LoadImage
from Works.FlushKey import FlushKey
from DataControl.Repo import load_blog_list
from queue import Queue
from time import sleep

# blog_list = load_blog_list()
#
# work_queue = Queue()
# for blog in blog_list:
#     for offset in range(21):
#         load_image = LoadImage(blog.url, offset=offset)
#         work_queue.put(load_image)
#
# while not work_queue.empty():
#     for i in range(10):
#         work = work_queue.get()
#         work.start()
#     sleep(5)
#
# while True:
#     continue
f = FlushKey()
f.start()
f.join()
# while True:
#     continue
