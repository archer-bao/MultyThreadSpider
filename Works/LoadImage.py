from threading import Thread
from tumblpy import Tumblpy
from DataControl.Key import get_key, update_key_use
from Config import spider_log


class LoadImage(Thread):
    offset = 0
    blog_url = ""
    key = None

    def __init__(self, blog_url, offset):
        super(LoadImage, self).__init__()
        self.blog_url = blog_url
        self.offset = offset
        self._load_key()

    def _load_key(self):
        self.key = get_key()
        spider_log.info("加载Key完成！KeyId:{}".format(self.key.id))

    @update_key_use
    def run(self):
        spider_log.info("开始获取图片！Blog:{} Offset:{}".format(self.blog_url, self.offset))
        t = Tumblpy(self.key.ConsumerKey, self.key.ConsumerSecret)
        t.client.verify = False
        posts = t.get('posts', blog_url=self.blog_url, params={"offset": self.offset})
        print(posts)
        t.client.close()
