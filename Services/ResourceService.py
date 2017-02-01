from queue import Queue
from tumblpy import Tumblpy
from DAOs.BlogDao import get_blog_list
from DAOs.KeyDao import get_key_list, get_oldest_key
from DAOs.PublicDao import commit
from DAOs.RepoDao import same_item_count, add_item
from datetime import datetime
from Objects.Image import Image
from Objects.Video import Video
from Config import log
from SpiderException.SpiderException import SpiderException


def video_posts_handler(posts, blog):
    for post in posts:
        url = post.get('video_url')
        release_time = post.get('date')[:19]
        if url is None:
            log.info("Video has been removed jump to next.")
            continue
        else:
            video = Video(url, blog.id, release_time)
        if same_item_count(Video, video) > 0:
            log.info("Video:{} already exist.".format(video.url))
            raise SpiderException("This object already exist.")
        else:
            add_item(video)
            log.info("Video:{} add to database successful.".format(video.url))


def image_posts_handler(posts, blog):
    for post in posts:
        photo_list = post.get('photos')
        release_time = post.get('date')[:19]
        for photo in photo_list:
            alt_sizes = photo.get('alt_sizes')
            photo_item = alt_sizes[0]
            photo_url = photo_item.get('url')
            image = Image(photo_url, blog.id, release_time)
            if same_item_count(Image, image) > 0:
                log.info("Image:{} already exist.".format(image.url))
                raise SpiderException("This object already exist.")
            else:
                add_item(image)
                log.info("Image:{} add to database successful.".format(image.url))


def load_blog():
    blogs = get_blog_list()
    log.info("Load {} blogs.".format(str(len(blogs))))
    return to_queue(blogs)


def load_key():
    keys = get_key_list()
    log.info("Load {} keys.".format(str(len(keys))))
    return to_queue(keys)


def to_queue(items):
    item_queue = Queue()
    for item in items:
        item_queue.put(item)
    log.info("Add {} items to {} queue.".format(str(len(items)), items[0].__class__))
    return item_queue


def blog_died(blog):
    blog.alive = 0
    commit()


def token_expire():
    key = get_oldest_key()
    if (datetime.now() - key.UpdateTime).days >= 7:
        return True
    else:
        return False


def update_token():
    key_queue = load_key()
    while not key_queue.empty():
        key = key_queue.get()
        t = Tumblpy(key.ConsumerKey, key.ConsumerSecret)
        auth_props = t.get_authentication_tokens(callback_url='https://www.google.com.sg')
        key.TokenSecret = auth_props.get("oauth_token_secret")
        key.Token = auth_props.get("oauth_token")
        key.UpdateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit()
    log.info("Keys are updated.")


def load_resource():
    return {
        "blog_queue": load_blog(),
        "key_queue": load_key()
    }
