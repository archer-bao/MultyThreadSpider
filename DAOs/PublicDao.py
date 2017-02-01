from Data.Database import DATABASE_SESSION


def commit():
    DATABASE_SESSION.commit()
