import shutil
from bark.config.config import BarkConfig
from bark.util.logger import BarkLogger
from bark.ui.title_widget import TitleWidget
from bark.ui.stream_widget import StreamWidget
from bark.ui.prompt_widget import PromptWidget
from bark.ui.command_widget import CommandWidget
from bark.ui.status_widget import StatusWidget


class BarkUI:
 
    def __init__(self, api):
        self.api = api
        self.config = BarkConfig(None)
        self.logger = BarkLogger(__file__)
        self.printed_lines = 0
        self.progress = None

    def build_ui(self, stdscr):
        terminal_size = shutil.get_terminal_size()
        self.terminal_width = terminal_size[0]
        self.terminal_height = terminal_size[1]

        # Clear screen
        stdscr.clear()

        # Add Title Widget
        self.title_widget = TitleWidget('Bark Twitter Client', 0, 0)

        # Add Strean Widget
        self.stream_widget = StreamWidget(1, 0)

        # Add Prompt Widget
        self.prompt_widget = PromptWidget('username', self.terminal_height-3, 0)

        # Add Command Widget
        self.command_widget = CommandWidget(self.terminal_height-3, self.prompt_widget.get_prompt_width())

        # Add Status Widget
        self.status_widget = StatusWidget(self.terminal_height-2, 0)

        self.refresh_stream()
        while True:
            command = self.command_widget.get_command(self.validate_input)

    def validate_input(self, char):
        if char == 338:
            self.do_page_down()
        elif char == 339:
            self.do_page_up()
        return char

    def do_page_up(self):
        self.logger.debug('Doing Page Up %d' % self.stream_widget.scroll_current)
        scroll_new = self.stream_widget.scroll_current-(self.terminal_height-4)
        if scroll_new < 0:
            scroll_new = 0
        self.stream_widget.scroll_to(scroll_new)

    def do_page_down(self):
        scroll_max = self.stream_widget.printed_lines - (self.terminal_height) + 4
        self.logger.debug('Doing Page Down %d' % self.stream_widget.scroll_current)
        scroll_new = self.stream_widget.scroll_current+(self.terminal_height-4)
        if scroll_new > scroll_max:
            scroll_new = scroll_max
        self.stream_widget.scroll_to(scroll_new)

    def refresh_stream(self):
        time_line_statuses = self.api.GetHomeTimeline(count=100, since_id=self.progress)
        self.stream_widget.refresh_stream(time_line_statuses)
