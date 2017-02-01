from Init import SPIDER_DATABASE


class Blog(SPIDER_DATABASE.Model):
    __tablename__ = "blog"
    id = SPIDER_DATABASE.Column(SPIDER_DATABASE.Integer, autoincrement=True, primary_key=True, unique=True)
    url = SPIDER_DATABASE.Column(SPIDER_DATABASE.String)
    name = SPIDER_DATABASE.Column(SPIDER_DATABASE.String)
    code = SPIDER_DATABASE.Column(SPIDER_DATABASE.Integer)
    alive = SPIDER_DATABASE.Column(SPIDER_DATABASE.Integer)
