import logging
import os
from bark.config.config import BarkConfig

class BarkLogger:

    def __init__(self, filename):
        config = BarkConfig(None)
        self.logger = logging.getLogger(filename)
       
        #Allow overriding the log file- Mainly used for testing
        if config.get_value('LOGGING', 'logfile') != None:
            hdlr = logging.FileHandler(config.get_value('LOGGING', 'logfile'))
        else:
            hdlr = logging.FileHandler('bark.log')

        formatter = logging.Formatter('%(asctime)s '+os.path.basename(filename)+' %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        if config.get_value('LOGGING', 'loglevel') == 'debug':
            self.logger.setLevel(logging.DEBUG)
        elif config.get_value('LOGGING', 'loglevel') == 'error':
            self.logger.setLevel(logging.ERROR)
        else:
            self.logger.setLevel(logging.INFO)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)
