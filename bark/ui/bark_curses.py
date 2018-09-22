import sys
import shutil
import curses
import logging
from curses.textpad import Textbox
from bark.ui.rendering import Render

class BarkCurses:

    def __init__(self, api):
        self.api = api
        self.renderer = Render()
        self.logger = logging.getLogger(__file__)
        hdlr = logging.FileHandler(__file__ + ".log")
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)

    def main(self, stdscr):
        terminal_size = shutil.get_terminal_size()
        self.terminal_width = terminal_size[0]
        self.terminal_height = terminal_size[1]

        # Clear screen
        stdscr.clear()

        #Create the timeline window
        self.timeline_win = self.create_timeline_win()

        #Create the Prompt
        credentials = self.api.VerifyCredentials()
        prompt_win, prompt_width = self.create_prompt_win(credentials.name)
        prompt_win.refresh()

        #Create Input window
        edit_line_win = self.create_edit_line_win(prompt_width)
        box = Textbox(edit_line_win)
        box.stripspaces = 1
        self.do_refresh()
        while True:
            box.edit()
            message = box.gather()
            edit_line_win.clear()
            self.handle_command(message)

    def create_timeline_win(self):
        return curses.newpad(2000, self.terminal_width)

    def create_prompt_win(self, username):
        prompt_width = len(username)+4
        prompt_win = curses.newwin(1, prompt_width, self.terminal_height-1, 0)
        prompt_win.addstr('[@'+username+']')
        return prompt_win, prompt_width

    def create_edit_line_win(self, prompt_width):
        win = curses.newwin(1, self.terminal_width, self.terminal_height-1, prompt_width)
        return win

    def handle_command(self, message):
        stripped_message = message.strip()
        if stripped_message.lower() == "refresh":
            self.do_refresh()
        elif stripped_message.lower() == "exit":
            sys.exit()

    def do_refresh(self):
        time_line_statuses = self.api.GetHomeTimeline(count=50)
        time_column_width = 9
        username_column_width = self.renderer.get_longest_username(time_line_statuses)
        text_column_width = self.terminal_width - username_column_width - 12
        tweets = []
        for status in reversed(time_line_statuses):
            tweet = self.renderer.render_tweet(status, text_column_width)
            tweets.append(tweet)

        pminrow = self.terminal_height - 1
        pmincol = 0
        sminrow = 0
        smincol = 0
        smaxrow = self.terminal_height - 2
        smaxcol = self.terminal_width
        self.logger.debug('pminrow = %d' % pminrow)
        self.logger.debug('pmincol = %d' % pmincol)
        self.logger.debug('sminrow = %d' % sminrow)
        self.logger.debug('smincol = %d' % smincol)
        self.logger.debug('smaxrow = %d' % smaxrow)
        self.logger.debug('smaxcol = %d' % smaxcol)
        first_line = len(tweets)-smaxrow
        last_line = len(tweets)
        self.timeline_win.clear()
        printed_lines = self._print_tweets(time_column_width, username_column_width, first_line, last_line, tweets)
        self.timeline_win.refresh(pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol)

    def _print_tweets(self, time_column_width, username_column_width, first_line, last_line, tweets):
        first_column_width = time_column_width + username_column_width + 2
        printed_lines = 0
        for tweet in tweets:
            self.timeline_win.addstr('%s %s | %s\n' % (tweet['time'], tweet['username'].rjust(username_column_width), tweet['tweet_lines'][0]))
            printed_lines += printed_lines
            for line in tweet['tweet_lines'][1:]:
                self.timeline_win.addstr('%s %s\n' % ('|'.rjust(first_column_width), line))
                printed_lines += printed_lines
        return printed_lines
