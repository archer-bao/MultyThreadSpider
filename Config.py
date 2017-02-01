from Objects.Logger import Logger

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:liqing@localhost:3306/spider"
log = Logger('SpiderLog.log', 'SpiderLog').get_log()
