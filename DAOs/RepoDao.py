from Data.Database import DATABASE_SESSION
from DAOs.PublicDao import commit
from sqlalchemy import func


def add_item(item):
    DATABASE_SESSION.add(item)
    commit()


def same_item_count(class_name, obj):
    return DATABASE_SESSION.query(func.count('*')).select_from(class_name).filter_by(url=obj.url,
                                                                                     blog_id=obj.blog_id).scalar()
