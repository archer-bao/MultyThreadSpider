from Data.Database import DATABASE
from datetime import datetime


class Image(DATABASE.Model):
    __tablename__ = "image"
    id = DATABASE.Column(DATABASE.Integer, autoincrement=True, primary_key=True, unique=True)
    url = DATABASE.Column(DATABASE.String)
    path = DATABASE.Column(DATABASE.String)
    blog_id = DATABASE.Column(DATABASE.Integer)
    add_time = DATABASE.Column(DATABASE.DateTime)
    release_time = DATABASE.Column(DATABASE.DateTime)
    load_times = DATABASE.Column(DATABASE.Integer)
    like_times = DATABASE.Column(DATABASE.Integer)
    dislike_times = DATABASE.Column(DATABASE.Integer)

    def __init__(self, url, blog_id, release_time):
        self.url = url
        self.blog_id = blog_id,
        self.release_time = release_time
        self.add_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.load_times = 0
        self.like_times = 0
        self.dislike_times = 0
