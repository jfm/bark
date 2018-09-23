import configparser
from pathlib import Path
from bark.util.logger import Logger

class BarkConfig:
    def __init__(self):
        self.logger = Logger(__file__)
        self.config_file = None
        home = str(Path.home())
        self.config_parser = configparser.ConfigParser()
        user_config_file = Path(home + '/.config/bark/bark.conf')
        current_config_file = Path('bark.conf')
        if Path.exists(user_config_file):
            self.config_file = user_config_file
        elif Path.exists(current_config_file):
            self.config_file = current_config_file
        else:
            self.logger.info('No config files found - Creating a new one in: %s' % str(user_config_file))
            self.set_value('LOGGING', 'logfile', 'bark.log')
            self.set_value('LOGGING', 'loglevel', 'info')
        self.config_parser.read(str(self.config_file))

    def get_value(self, section, key):
        return self.config_parser[section][key]

    def set_value(self, section, key, value):
        cfgfile = open(str(self.config_file), 'w')
        self.config_parser[section][key] = value
        self.config_parser.write(cfgfile)
        cfgfile.close()
