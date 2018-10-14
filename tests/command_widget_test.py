import curses
from bark.ui.command_widget import CommandWidget

class TestCommandWidget:
    def setup_method(self, method):
        curses.initscr()
        self.command_widget = CommandWidget(1, 1)
