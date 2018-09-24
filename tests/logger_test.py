from bark.util.logger import BarkLogger
from pathlib import Path

class TestLoggerClass:

    def setup_method(self, method):
        if Path.exists(Path('test.log')):
            os.remove("test.log")

    def teardown_method(self, method):
        if Path.exists(Path('test.log')):
            os.remove("test.log")

    def test_debug(self, caplog):
        logger = BarkLogger(__file__)
        logger.debug('TEST DEBUG MESSAGE')
        for record in caplog.records:
            assert record.levelname == 'DEBUG'
            assert record.message == 'TEST DEBUG MESSAGE'

    def test_error(self, caplog):
        logger = BarkLogger(__file__)
        logger.error('TEST ERROR MESSAGE')
        for record in caplog.records:
            assert record.levelname == 'ERROR'
            assert record.message == 'TEST ERROR MESSAGE'

    def test_info(self, caplog):
        logger = BarkLogger(__file__)
        logger.info('TEST INFO MESSAGE')
        for record in caplog.records:
            assert record.levelname == 'INFO'
            assert record.message == 'TEST INFO MESSAGE'
