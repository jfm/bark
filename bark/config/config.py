import configparser
from pathlib import Path

class BarkConfig:
    def __init__(self, config_file_override):
        self.config_file = None
        home = str(Path.home())
        self.config_parser = configparser.ConfigParser()
        user_config_file = Path(home + '/.config/bark/bark.conf')
        #Allow overriding the name of the config file. Mainly used for testing
        if config_file_override == None:
            current_config_file = Path('bark.conf')
        else:
            current_config_file = Path(config_file_override)

        if Path.exists(user_config_file):
            self.config_file = user_config_file
        elif Path.exists(current_config_file):
            self.config_file = current_config_file
        else:
            self.config_file = current_config_file
            print('No config files found - Creating a new one in: %s' % str(user_config_file))
            self.set_value('LOGGING', 'logfile', 'bark.log')
            self.set_value('LOGGING', 'loglevel', 'info')
        self.config_parser.read(str(self.config_file))

    def get_value(self, section, key):
        if self.config_parser.has_option(section, key):
            return self.config_parser[section][key]
        else:
            return None

    def set_value(self, section, key, value):
        cfgfile = open(str(self.config_file), 'w')
        if not self.config_parser.has_section(section):
            self.config_parser.add_section(section)
        self.config_parser.set(section, key, value)
        self.config_parser.write(cfgfile)
        cfgfile.close()
        print('Wrote config file %s' % self.config_file)
