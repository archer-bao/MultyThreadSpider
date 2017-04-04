from threading import Thread

from tumblpy import Tumblpy
from tumblpy.exceptions import TumblpyRateLimitError, TumblpyError

from Config import spider_log, session
from DataControl.Key import get_key
from DataControl.Repo import mark_dead_blog, load_all_blog
from urllib.parse import urlparse


class UpdateBlog(Thread):
    def __init__(self):
        super(UpdateBlog, self).__init__()
        self._load_key()

    def _load_key(self):
        self.key = get_key()
        spider_log.info("加载Key完成！KeyId:{}".format(self.key.id))

    def run(self):
        spider_log.info("开始获取博客信息！")
        blogs = load_all_blog()
        spider_log.info("加载Blog列表完成！")
        for blog in blogs:
            print(blog.url)
            try:
                t = Tumblpy(self.key.ConsumerKey, self.key.ConsumerSecret)
                resp = t.get('info', blog_url=urlparse(blog.url).path)
                b = resp.get("blog")
                blog.title = b.get("title")
                blog.name = b.get("name")
                blog.alive = 1
                blog.loaded = 0
                blog.url = b.get("url")
                t.client.close()
            except TumblpyRateLimitError:
                spider_log.info("Key达到上限,本线程退出")
            except TumblpyError as e:
                if e.error_code == 404:
                    mark_dead_blog(blog)
            finally:
                session.commit()
                session.remove()


if __name__ == '__main__':
    pass
