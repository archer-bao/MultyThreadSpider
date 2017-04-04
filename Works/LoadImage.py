from threading import Thread
from tumblpy import Tumblpy
from tumblpy.exceptions import TumblpyRateLimitError, TumblpyError
from Config import spider_log, session
from DataControl.Key import get_key, update_key_use
from DataControl.Repo import same_item_count, add_item, update_blog_load, mark_dead_blog, get_blog
from Obj.Image import Image


class LoadImage(Thread):
    offset = 0
    blog_id = None

    def __init__(self, blog_id, offset):
        super(LoadImage, self).__init__()
        self.blog_id = blog_id
        self.offset = offset
        self._load_key()

    def _load_key(self):
        self.key = get_key()
        spider_log.debug("加载Key完成！KeyId:{}".format(self.key.id))

    def _load_blog(self):
        self.blog = get_blog(self.blog_id)
        spider_log.info("加载Blog完成！BlogId:{}".format(self.blog.id))

    @update_blog_load
    def run(self):
        self._load_blog()
        spider_log.info("开始获取图片！Blog:{} Offset:{}".format(self.blog.url, self.offset))

        @update_key_use(self.key)
        def do():
            try:
                t = Tumblpy(self.key.ConsumerKey, self.key.ConsumerSecret)
                t.client.verify = False
                resp = t.get('posts/photo', blog_url=self.blog.url, params={"offset": self.offset})
                posts = resp.get('posts')
                post_handler(posts, self.blog)
                t.client.close()
            except TumblpyRateLimitError:
                spider_log.info("Key达到上限,本线程退出")
                return
            except TumblpyError as e:
                if e.error_code == 404:
                    mark_dead_blog(self.blog)
            finally:
                session.remove()

        return do()


def post_handler(posts, blog):
    for post in posts:
        photo_list = post.get('photos')
        release_time = post.get('date')[:19]
        for photo in photo_list:
            alt_sizes = photo.get('alt_sizes')
            photo_item = alt_sizes[0]
            photo_url = photo_item.get('url')
            image = Image(photo_url, blog.id, release_time)
            if same_item_count(Image, image) > 0:
                spider_log.info("Image:{} already exist.".format(image.url))
            else:
                add_item(image)
                spider_log.info("Image:{} add to database successful.".format(image.url))
