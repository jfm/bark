import curses
from bark.ui.prompt_widget import PromptWidget

class TestPromptWidget:
    def setup_method(self, method):
        curses.initscr()
        self.prompt_widget = PromptWidget('username', 1, 1)

    def test_correct_prompt(self):
        assert self.prompt_widget.prompt_text == '[@username]'

    def test_get_prompt_width(self):
        assert self.prompt_widget.get_prompt_width() == 12
