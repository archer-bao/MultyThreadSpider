class SpiderException(Exception):
    @property
    def msg(self):
        return self.args[0]
