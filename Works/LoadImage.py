from threading import Thread
from tumblpy import Tumblpy
from DataControl.Key import get_key, update_key_use
from DataControl.Repo import same_item_count, add_item, update_blog_load, mark_dead_blog
from Config import spider_log, session
from Obj.Image import Image
from Excep import SpiderException
from tumblpy.exceptions import TumblpyRateLimitError, TumblpyError


class LoadImage(Thread):
    offset = 0
    blog = None
    key = None

    def __init__(self, blog, offset):
        super(LoadImage, self).__init__()
        self.blog = blog
        self.offset = offset
        self._load_key()

    def _load_key(self):
        self.key = get_key()
        spider_log.info("加载Key完成！KeyId:{}".format(self.key.id))

    @update_blog_load
    @update_key_use
    def run(self):
        spider_log.info("开始获取图片！Blog:{} Offset:{}".format(self.blog.url, self.offset))
        try:
            t = Tumblpy(self.key.ConsumerKey, self.key.ConsumerSecret)
            t.client.verify = False
            resp = t.get('posts/photo', blog_url=self.blog.url, params={"offset": self.offset})
            posts = resp.get('posts')
            post_handler(posts, self.blog)
            t.client.close()
        except SpiderException as e:
            spider_log.info(e.msg)
        except TumblpyRateLimitError:
            spider_log.info("Key达到上限,本线程退出")
            return
        except TumblpyError as e:
            if e.error_code == 404:
                mark_dead_blog(self.blog)
        finally:
            session.remove()


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
                raise SpiderException(msg="Object already exist")
            else:
                add_item(image)
                spider_log.info("Image:{} add to database successful.".format(image.url))
