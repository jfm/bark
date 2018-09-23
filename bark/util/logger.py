import logging
import os

class Logger:

    def __init__(self, filename):
        self.logger = logging.getLogger(filename)
        hdlr = logging.FileHandler("bark.log")
        formatter = logging.Formatter('%(asctime)s '+os.path.basename(filename)+' %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)
