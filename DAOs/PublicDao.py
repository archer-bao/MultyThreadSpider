from Init import SPIDER_DATABASE_SESSION


def commit():
    SPIDER_DATABASE_SESSION.commit()
