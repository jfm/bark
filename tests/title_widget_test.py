import curses
from bark.ui.title_widget import TitleWidget

class TestTitleWidget:
    def setup_method(self, method):
        curses.initscr()
        curses.start_color()
        self.title_widget = TitleWidget('title', 1, 1)

    def test_set_title_normal(self):
        title_text = self.title_widget.set_title('short title')
        assert title_text == 'short title'

    def test_set_title_long(self):
        self.title_widget.terminal_width = 10
        title_text = self.title_widget.set_title('short title')
        assert title_text == 'short ...'
