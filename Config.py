from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from Logger import Logger

DATABASE_URI = "mysql+pymysql://root:liqing@localhost:3306/spider"
session = scoped_session(sessionmaker(bind=create_engine(DATABASE_URI, echo=False, pool_size=20, max_overflow=0)))
BaseModel = declarative_base()
spider_log = Logger('spiderLog.log', 'spiderLog').get_log()
resource_folder = "/root/output/resources/"
