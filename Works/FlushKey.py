from threading import Thread
from tumblpy import Tumblpy
from DataControl.Key import get_all_key, update_key_use
from Config import spider_log, session
from datetime import datetime


class FlushKey(Thread):
    key = None

    def __init__(self):
        super(FlushKey, self).__init__()

    def run(self):
        spider_log.info("刷新Key中...")
        key_list = get_all_key()
        spider_log.info("加载Key列表完成！")
        for key in key_list:
            self.key = key
            self.flush_key()
        spider_log.info("刷新Key全部完成")

    @update_key_use
    def flush_key(self):
        spider_log.info("正在刷新Key ID:{}".format(self.key.id))
        t = Tumblpy(self.key.ConsumerKey, self.key.ConsumerSecret)
        auth_props = t.get_authentication_tokens()
        self.key.Token = auth_props.get("oauth_token")
        self.key.TokenSecret = auth_props.get("oauth_token_secret")
        self.key.UpdateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        t.client.close()
        session.commit()
        spider_log.info("刷新Key ID:{} 完成".format(self.key.id))
