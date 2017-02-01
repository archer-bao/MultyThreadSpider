from Data.Database import DATABASE


class Blog(DATABASE.Model):
    __tablename__ = "blog"
    id = DATABASE.Column(DATABASE.Integer, autoincrement=True, primary_key=True, unique=True)
    url = DATABASE.Column(DATABASE.String)
    name = DATABASE.Column(DATABASE.String)
    code = DATABASE.Column(DATABASE.Integer)
    alive = DATABASE.Column(DATABASE.Integer)
