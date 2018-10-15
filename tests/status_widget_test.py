import curses
from bark.ui.status_widget import StatusWidget

class TestStatusWidget:
    def setup_method(self, method):
        curses.initscr()
        curses.start_color()
        self.status_widget = StatusWidget(1, 1)

    def test_set_status(self):
        status_message = self.status_widget.set_status_text('status text')
        assert status_message == 'status text'
