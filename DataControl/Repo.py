from Config import session
from Obj.Blog import Blog


def add_image(image):
    session.add(image)
    session.commit()


def load_blog_list():
    return session.query(Blog).filter(Blog.alive == 1, Blog.loaded == 0).all()
