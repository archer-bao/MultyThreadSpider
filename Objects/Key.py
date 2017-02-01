from Data.Database import DATABASE


class Key(DATABASE.Model):
    __tablename__ = 'key'
    id = DATABASE.Column(DATABASE.Integer, primary_key=True, autoincrement=True, unique=True)
    ConsumerKey = DATABASE.Column(DATABASE.String)
    ConsumerSecret = DATABASE.Column(DATABASE.String)
    Token = DATABASE.Column(DATABASE.String)
    TokenSecret = DATABASE.Column(DATABASE.String)
    UpdateTime = DATABASE.Column(DATABASE.DateTime)
    UseTimes = DATABASE.Column(DATABASE.Integer)

    def __init__(self, consumer_key, consumer_secret):
        self.ConsumerKey = consumer_key
        self.ConsumerSecret = consumer_secret
