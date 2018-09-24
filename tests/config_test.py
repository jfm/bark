import os
from bark.config.config import BarkConfig
from pathlib import Path

class TestConfigClass:
    def setup_method(self, method):
        if Path.exists(Path('test.conf')):
            os.remove("test.conf")

    def teardown_method(self, method):
        if Path.exists(Path('test.conf')):
            os.remove("test.conf")

    def test_init(self):
        config = BarkConfig('test.conf')
        assert self.check_exists('test.conf') == True
        assert config.get_value('LOGGING', 'logfile') == 'bark.log'
        assert config.get_value('LOGGING', 'loglevel') == 'info'

    def test_set_and_get(self):
        config = BarkConfig('test.conf')
        config.set_value('TEST', 'test', 'testvalue')
        assert config.get_value('TEST', 'test') == 'testvalue'

    def check_exists(self, filename):
        if Path.exists(Path(filename)):
            return True
        else:
            return False
