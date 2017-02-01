from Init import SPIDER_DATABASE


class Key(SPIDER_DATABASE.Model):
    __tablename__ = 'key'
    id = SPIDER_DATABASE.Column(SPIDER_DATABASE.Integer, primary_key=True, autoincrement=True, unique=True)
    ConsumerKey = SPIDER_DATABASE.Column(SPIDER_DATABASE.String)
    ConsumerSecret = SPIDER_DATABASE.Column(SPIDER_DATABASE.String)
    Token = SPIDER_DATABASE.Column(SPIDER_DATABASE.String)
    TokenSecret = SPIDER_DATABASE.Column(SPIDER_DATABASE.String)
    UpdateTime = SPIDER_DATABASE.Column(SPIDER_DATABASE.DateTime)
    UseTimes = SPIDER_DATABASE.Column(SPIDER_DATABASE.Integer)

    def __init__(self, consumer_key, consumer_secret):
        self.ConsumerKey = consumer_key
        self.ConsumerSecret = consumer_secret
