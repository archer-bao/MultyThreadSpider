import logging


class Logger:
    def __init__(self, log_file_name, logger):
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.INFO)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(log_file_name)
        fh.setLevel(logging.INFO)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_log(self):
        return self.logger

    def destroy_log(self):
        self.logger.handlers = []


if __name__ == '__main__':
    log = Logger('test', 'mylog').get_log()
    log.info('this is a test log')
