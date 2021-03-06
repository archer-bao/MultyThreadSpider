from Config import session
from Obj.Blog import Blog
from sqlalchemy import func, not_


def load_download_item(class_name):
    item_list = session.query(class_name).filter_by(file_path=None).all()
    return item_list


def load_all_downloaded_item(class_name):
    item_list = session.query(class_name).filter(not_(class_name.file_path is None)).all()
    return item_list


def get_item(class_name, id):
    return session.query(class_name).get(id)


def get_blog(id):
    return session.query(Blog).get(id)


def get_item_blog(item):
    return session.query(Blog).get(item.blog_id)


def load_alive_blog_list():
    return session.query(Blog).filter(Blog.alive == 1).all()


def load_all_blog():
    return session.query(Blog).all()


def same_item_count(class_name, obj):
    return session.query(func.count('*')).select_from(class_name).filter_by(url=obj.url, blog_id=obj.blog_id).scalar()


def mark_dead_blog(blog):
    b = session.query(Blog).with_lockmode('update').get(blog.id)
    b.alive = 0
    session.commit()


def update_blog_load_image(func):
    def wrapper(*args, **kwargs):
        b = session.query(Blog).with_lockmode('update').get(args[0].blog_id)
        b.loaded_image += 1
        session.commit()

        return func(*args, **kwargs)

    return wrapper


def update_blog_load_video(func):
    def wrapper(*args, **kwargs):
        b = session.query(Blog).with_lockmode('update').get(args[0].blog_id)
        b.loaded_video += 1
        session.commit()

        return func(*args, **kwargs)

    return wrapper


def add_item(item):
    session.add(item)
    session.commit()
