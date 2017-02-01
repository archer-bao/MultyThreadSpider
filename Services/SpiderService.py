from Services.ResourceService import video_posts_handler, load_resource, blog_died, update_token, token_expire, \
    image_posts_handler
from tumblpy import Tumblpy
from tumblpy.exceptions import TumblpyError
from Config import log
from Services.LogService import use_key
from SpiderException.SpiderException import SpiderException


def init_spider():
    log.info("Start init spider.")
    if token_expire():
        log.info("Token were expire. Updating...")
        update_token()
        log.info("Start load resource.")
    return load_resource()


@use_key
def load_image(**kwargs):
    t = Tumblpy(kwargs.get("apikey").ConsumerKey, kwargs.get("apikey").ConsumerSecret)

    log.info("Start load photo posts of {} offset: {}".format(kwargs.get("blog").url, kwargs.get("offset")))
    try:
        resp = t.get('posts/photo', blog_url=kwargs.get("blog").url,
                     params={"offset": kwargs.get("offset"), "limit": 20})
        posts = resp.get('posts')
        log.info("Receive {} photo posts successful.".format(str(len(posts))))
        image_posts_handler(posts, kwargs.get("blog"))
    except TumblpyError as e:
        if e.error_code == 404:
            log.info("{} was died.".format(kwargs.get("blog").url))
            blog_died(kwargs.get("blog"))
        else:
            raise TumblpyError
    except SpiderException:
        return


@use_key
def load_video(**kwargs):
    t = Tumblpy(kwargs.get("apikey").ConsumerKey, kwargs.get("apikey").ConsumerSecret)

    # t = Tumblpy(kwargs.get("apikey").ConsumerKey, kwargs.get("apikey").ConsumerSecret,
    #             proxies={'http': "socks5://127.0.0.1:1080", 'https': "socks5://127.0.0.1:1080"}
    #             )
    log.info("Start load video posts of {} offset: {}".format(kwargs.get("blog").url, kwargs.get("offset")))
    try:
        resp = t.get('posts/video', blog_url=kwargs.get("blog").url,
                     params={"offset": kwargs.get("offset"), "limit": 20})
        posts = resp.get('posts')
        log.info("Receive {} video posts successful.".format(str(len(posts))))
        video_posts_handler(posts, kwargs.get("blog"))
    except TumblpyError as e:
        if e.error_code == 404:
            log.info("{} was died.".format(kwargs.get("blog").url))
            blog_died(kwargs.get("blog"))
        else:
            raise TumblpyError
    except SpiderException:
        return
