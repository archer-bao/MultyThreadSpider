from Init import SPIDER_DATABASE
from datetime import datetime


class Video(SPIDER_DATABASE.Model):
    __tablename__ = "video"
    id = SPIDER_DATABASE.Column(SPIDER_DATABASE.Integer, autoincrement=True, primary_key=True, unique=True)
    url = SPIDER_DATABASE.Column(SPIDER_DATABASE.String)
    path = SPIDER_DATABASE.Column(SPIDER_DATABASE.String)
    blog_id = SPIDER_DATABASE.Column(SPIDER_DATABASE.Integer)
    add_time = SPIDER_DATABASE.Column(SPIDER_DATABASE.DateTime)
    release_time = SPIDER_DATABASE.Column(SPIDER_DATABASE.DateTime)
    load_times = SPIDER_DATABASE.Column(SPIDER_DATABASE.Integer)
    like_times = SPIDER_DATABASE.Column(SPIDER_DATABASE.Integer)
    dislike_times = SPIDER_DATABASE.Column(SPIDER_DATABASE.Integer)

    def __init__(self, url, blog_id, release_time):
        self.url = url
        self.blog_id = blog_id,
        self.release_time = release_time
        self.add_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.load_times = 0
        self.like_times = 0
        self.dislike_times = 0
