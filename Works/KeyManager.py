from datetime import datetime, timedelta

from tumblpy import Tumblpy

from Config import spider_log, session
from DataControl.Key import get_all_key, get_newest_key


def do_flush_key(key):
    spider_log.info("正在刷新Key ID:{}".format(key.id))
    t = Tumblpy(key.ConsumerKey, key.ConsumerSecret)
    auth_props = t.get_authentication_tokens()
    key.Token = auth_props.get("oauth_token")
    key.TokenSecret = auth_props.get("oauth_token_secret")
    spider_log.info("请打开下面的链接执行授权")
    spider_log.info(auth_props.get("auth_url"))
    key.UpdateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    t.client.close()
    session.commit()
    spider_log.info("刷新Key ID:{} 完成".format(key.id))


def flush_key(key_list):
    spider_log.info("刷新Key中...")
    for key in key_list:
        do_flush_key(key)
    spider_log.info("刷新Key全部完成")


def check_key():
    spider_log.info("检查Key中...")
    if not key_is_valid():
        key_list = get_all_key()
        flush_key(key_list)


def key_is_valid():
    newest_key = get_newest_key()
    return newest_key.UpdateTime - datetime.now() > timedelta(days=7)
