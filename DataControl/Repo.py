from Config import session
from Obj.Blog import Blog
from sqlalchemy import func


def load_download_item_and_blog_list(class_name):
    item_list = session.query(class_name).filter_by(path=None).all()
    return item_list


def get_item(class_name, id):
    return session.query(class_name).get(id)


def get_blog(id):
    return session.query(Blog).get(id)


def get_item_blog(item):
    return session.query(Blog).get(item.blog_id)


def load_blog_list():
    return session.query(Blog.id).filter(Blog.alive == 1, Blog.loaded == 0).all()


def load_all_blog():
    return session.query(Blog).all()


def same_item_count(class_name, obj):
    return session.query(func.count('*')).select_from(class_name).filter_by(url=obj.url, blog_id=obj.blog_id).scalar()


def mark_dead_blog(blog):
    b = session.query(Blog).with_lockmode('update').get(blog.id)
    b.alive = 0
    session.commit()


def update_blog_load(func):
    def wrapper(*args, **kwargs):
        if args[0].offset == 20:
            b = session.query(Blog).with_lockmode('update').get(args[0].blog_id)
            b.loaded = 1
            session.commit()
        return func(*args, **kwargs)

    return wrapper


def reset_blog_loaded():
    all_blog = load_all_blog()
    for blog in all_blog:
        if blog.alive == 1 and blog.loaded == 1:
            blog.loaded = 0
    session.commit()


def add_item(item):
    session.add(item)
    session.commit()
