import shutil
import sys
import curses
import threading
import time
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
        self.tweets = []

    def build_ui(self, stdscr):
        terminal_size = shutil.get_terminal_size()
        self.terminal_width = terminal_size[0]
        self.terminal_height = terminal_size[1]

        # Clear screen
        stdscr.clear()
        if curses.has_colors():
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
            curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

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

        self.refresh_thread = threading.Thread(target=self.refresh_thread_worker)
        self.refresh_thread.start()
        while True:
            command = self.command_widget.get_command(self.validate_input)
            self.handle_command(command)

    def validate_input(self, char):
        if char == 338:
            self.do_page_down()
        elif char == 339:
            self.do_page_up()
        return char

    def handle_command(self, message):
        if len(message) > 0:
            command_words = message.split()
            command = command_words[0].lower()
            self.logger.debug('Got Command: %s' % command)
            if command == "/refresh":
                self.refresh_stream()
            elif command == "/tweet":
                self.do_tweet(command_words[1:])
            elif command == "/heart":
                self.do_heart(command_words[1])
            elif command == "/retweet":
                self.do_retweet(command_words[1])
            elif command == "/exit":
                sys.exit()
            else:
                self.logger.debug('unknown command')
        else:
            self.logger.debug('Empty command')

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

    def do_tweet(self, words):
        tweet_message = ''
        for word in words:
            tweet_message = tweet_message + word + ' '

        if len(tweet_message) < 240:
            if self.config.get_value('CONFIGURATION','simulate_tweeting') == 'false':
                self.api.PostUpdate(tweet_message.strip())
            else:
                self.logger.info('Would have tweeted: |%s|' % tweet_message.strip())
            self.status_widget.set_status_text("Tweet send!")
        else:
            self.status_widget.set_status_text("Tweet too long (%d characters)" % len(tweet_message))

    def do_heart(self, index_text):
        try:
            index = int(index_text)
            self.logger.info('Hearting %d - %s' % (index, self.tweets[index]['id']))
            self.api.CreateFavorite(status_id=self.tweets[index]['id'])
        except ValueError:
            self.status_widget.set_status_text('Could not heart tweet! Use Example: /heart 005')

    def do_retweet(self, index_text):
        try:
            index = int(index_text)
            self.logger.info('Retweeting %d - %s' % (index, self.tweets[index]['id']))
            self.api.PostRetweet(self.tweets[index]['id'])
        except ValueError:
            self.status_widget.set_status_text('Could not retweet! Use Example: /retweet 005')

    def refresh_thread_worker(self):
        while True:
            self.logger.debug("Refreshing")
            self.refresh_stream()
            time.sleep(300)

    def refresh_stream(self):
        time_line_statuses = self.api.GetHomeTimeline(count=100, since_id=self.progress)
        self.tweets, self.progress = self.stream_widget.refresh_stream(time_line_statuses)
