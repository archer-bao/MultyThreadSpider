from Objects.Blog import Blog
from Init import SPIDER_DATABASE_SESSION


def get_blog_list():
    return SPIDER_DATABASE_SESSION.query(Blog).filter(Blog.alive == 1).all()
