from threading import Thread
from tumblpy import Tumblpy
from tumblpy.exceptions import TumblpyRateLimitError, TumblpyError
from Config import spider_log, session
from DataControl.Key import get_key, update_key_use
from DataControl.Repo import same_item_count, add_item, update_blog_load_video, mark_dead_blog, get_blog
from Obj.Video import Video


class LoadVideo(Thread):
    offset = 0
    blog_id = None

    def __init__(self, blog_id, offset):
        super(LoadVideo, self).__init__()
        self.blog_id = blog_id
        self.offset = offset
        self._load_key()

    def _load_key(self):
        self.key = get_key()
        spider_log.debug("加载Key完成！KeyId:{}".format(self.key.id))

    def _load_blog(self):
        self.blog = get_blog(self.blog_id)
        spider_log.info("加载Blog完成！BlogId:{}".format(self.blog.id))

    @update_blog_load_video
    def run(self):
        self._load_blog()
        spider_log.info("Thread:{} 开始获取视频！Blog:{} Offset:{}".format(self.getName(), self.blog.url, self.offset))

        @update_key_use(self.key)
        def do():
            try:
                t = Tumblpy(self.key.ConsumerKey, self.key.ConsumerSecret)
                resp = t.get('posts/video', blog_url=self.blog.url, params={"offset": self.offset})
                # 视频不存在会导致 url字段为空
                posts = resp.get('posts')
                video_posts_handler(posts, self.blog)
                t.client.close()
            except TumblpyRateLimitError:
                spider_log.info("Key调用次数达到上限,本线程退出")
                return
            except TumblpyError as e:
                if e.error_code == 404:
                    mark_dead_blog(self.blog)
            finally:
                session.remove()

        return do()


def video_posts_handler(posts, blog):
    for post in posts:
        url = post.get('video_url')
        release_time = post.get('date')[:19]
        if url is None:
            spider_log.info("Video has been removed jump to next.")
            continue
        else:
            video = Video(url, blog.id, release_time)
        if same_item_count(Video, video) > 0:
            spider_log.info("Video:{} already exist.".format(video.url))
        else:
            add_item(video)
            spider_log.info("Video:{} add to database successful.".format(video.url))
