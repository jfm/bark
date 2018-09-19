import configparser
from pathlib import Path

class BarkConfig:
    def __init__(self):
        home = str(Path.home())
        self.config_parser = configparser.ConfigParser()
        user_config_file = Path(home + '/.config/bark/bark.conf')
        current_config_file = Path('bark.conf')
        if Path.exists(user_config_file):
            self.config_parser.read(str(user_config_file))
        else:
            if Path.exists(current_config_file):
               self.config_parser.read(str(current_config_file))
            else:
                print('No config files found')

    def get_value(self, section, key):
        return self.config_parser[section][key]
