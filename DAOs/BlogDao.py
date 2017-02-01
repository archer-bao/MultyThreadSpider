from Objects.Blog import Blog
from Data.Database import DATABASE_SESSION


def get_blog_list():
    return DATABASE_SESSION.query(Blog).filter(Blog.alive == 1).all()
