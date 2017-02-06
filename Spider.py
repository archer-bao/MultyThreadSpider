from Works.LoadImage import LoadImage
from DataControl.Repo import load_blog_list
from queue import Queue
from time import sleep
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

blog_list = load_blog_list()

work_queue = Queue()
for blog in blog_list:
    for offset in range(21):
        load_image = LoadImage(blog, offset=offset)
        work_queue.put(load_image)

while not work_queue.empty():
    for i in range(4):
        work = work_queue.get()
        work.start()

    sleep(5)




while True:
    continue
