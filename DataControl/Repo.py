from Config import session
from Obj.Blog import Blog
from sqlalchemy import func


def load_blog_list():
    return session.query(Blog).filter(Blog.alive == 1, Blog.loaded == 0).all()


def same_item_count(class_name, obj):
    return session.query(func.count('*')).select_from(class_name).filter_by(url=obj.url, blog_id=obj.blog_id).scalar()


def mark_dead_blog(blog):
    b = session.query(Blog).with_lockmode('update').get(blog.id)
    b.alive = 0
    session.commit()


def update_blog_load(func):
    def wrapper(*args, **kwargs):
        if args[0].offset == 20:
            b = session.query(Blog).with_lockmode('update').get(args[0].blog.id)
            b.loaded = 1
            session.commit()
            # session.remove()
        return func(*args, **kwargs)

    return wrapper


def reset_blog_loaded():
    alive_count = session.query(func.count('*')).select_from(Blog).filter(Blog.alive == 1).scalar()
    loaded_count = session.query(func.count('*')).select_from(Blog).filter(Blog.loaded == 1).scalar()
    if alive_count == loaded_count:
        session.query(Blog).with_lockmode('update').update({Blog.loaded: 0})


def add_item(item):
    session.add(item)
    session.commit()
    # session.remove()
