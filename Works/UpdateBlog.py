from threading import Thread
from urllib.parse import urlparse

from tumblpy import Tumblpy
from tumblpy.exceptions import TumblpyRateLimitError, TumblpyError

from Config import spider_log, session
from DataControl.Key import get_key
from DataControl.Key import update_key_use
from DataControl.Repo import mark_dead_blog, load_all_blog


class UpdateBlog(Thread):
    def __init__(self):
        super(UpdateBlog, self).__init__()
        self._load_key()

    def _load_key(self):
        self.key = get_key()
        spider_log.info("加载Key完成！KeyId:{}".format(self.key.id))

    def run(self):
        @update_key_use(self.key)
        def do():
            spider_log.info("开始获取博客信息！")
            blogs = load_all_blog()
            spider_log.info("加载Blog列表完成！")
            for blog in blogs:
                try:
                    t = Tumblpy(self.key.ConsumerKey, self.key.ConsumerSecret)
                    resp = t.get('info', blog_url=urlparse(blog.url).netloc)
                    b = resp.get("blog")
                    t.client.close()
                    blog.name = b.get("name")
                    blog.url = b.get("url")
                    blog.posts = b.get("posts")
                    spider_log.info("BlogId:{} 已更新".format(blog.id))
                except TumblpyRateLimitError:
                    spider_log.info("Key达到上限,本线程退出")
                except TumblpyError as e:
                    if e.error_code == 404:
                        mark_dead_blog(blog)
                finally:
                    session.commit()
            session.remove()

        return do()


if __name__ == '__main__':
    lo = UpdateBlog()
    lo.start()
    lo.join()
