from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String, DateTime
from Config import SQLALCHEMY_DATABASE_URI
from Objects.Logger import Logger

# ===========数据库===========
SPIDER_DATABASE = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
SPIDER_DATABASE_SESSION = sessionmaker(bind=SPIDER_DATABASE)()
SPIDER_DATABASE_BASE = declarative_base()
SPIDER_DATABASE.Model = SPIDER_DATABASE_BASE
SPIDER_DATABASE.Column = Column
SPIDER_DATABASE.Integer = Integer
SPIDER_DATABASE.String = String
SPIDER_DATABASE.DateTime = DateTime

# ===========日志===========
log = Logger('SpiderLog.log', 'SpiderLog').get_log()
# ============代理============
PROXIES = {'http': "socks5://127.0.0.1:1080", 'https': "socks5://127.0.0.1:1080"}
