import sys
import shutil
import curses
from curses.textpad import Textbox
from bark.ui.rendering import Render
from bark.util.logger import Logger

class BarkCurses:

    def __init__(self, api):
        self.api = api
        self.renderer = Render()
        self.logger = Logger(__file__)
        self.tweets = []
        self.printed_lines = 0
        self.progress = None

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
        prompt_win, prompt_width = self.create_prompt_win(credentials.screen_name)
        prompt_win.refresh()

        #Create Input window
        edit_line_win = self.create_edit_line_win(prompt_width)
        box = BarkTextbox(edit_line_win, self)
        box.stripspaces = 1
        
        #Refresh tweets and start loop
        self.do_refresh()
        while True:
            message = box.edit()
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
        else:
            self.logger.debug('unknown command')

    def do_page_up(self):
        self.logger.debug('Doing Page Up %d' % self.scroll_current)
        scroll_new = self.scroll_current-(self.terminal_height-1)
        if scroll_new < 0:
            scroll_new = 0
        self.scroll_to(scroll_new)

    def do_page_down(self):
        scroll_max = self.printed_lines - (self.terminal_height-2)
        self.logger.debug('Doing Page Down %d' % self.scroll_current)
        scroll_new = self.scroll_current+(self.terminal_height-1)
        if scroll_new > scroll_max:
            scroll_new = scroll_max
        self.scroll_to(scroll_new)

    def do_refresh(self):
        self.logger.debug('REFRESH: progress = %s' % self.progress)
        time_line_statuses = self.api.GetHomeTimeline(count=100, since_id=self.progress)

        #Set the column width of the Time Column
        time_column_width = 9

        #Set the column width of the Username Column
        if time_line_statuses is not None:
            usernames = []
            for tweet in self.tweets:
                usernames.append(tweet['username'])
            for status in time_line_statuses:
                usernames.append(status.user.screen_name)

            username_column_width = self.renderer.get_longest_username(usernames)

        #Set the column width of the Text Column
        text_column_width = self.terminal_width - username_column_width - 12

        #Build the rendered tweet objects
        for status in reversed(time_line_statuses):
            tweet = self.renderer.render_tweet(status, text_column_width)
            self.tweets.append(tweet)
            self.progress = tweet['id']

        self.timeline_win.clear()
        self.printed_lines = self.print_tweets(time_column_width, username_column_width, self.tweets)
        self.scroll_to(self.printed_lines-(self.terminal_height-1))

    def scroll_to(self, row):
        self.scroll_current = row
        pminrow = self.scroll_current
        pmincol = 0
        sminrow = 0
        smincol = 0
        smaxrow = self.terminal_height - 2
        smaxcol = self.terminal_width
        self.logger.debug('PAD REFRESH: pminrow = %d, pmincol = %d, sminrow = %d, smincol = %d, smaxrow = %d, smaxcol = %d' % (pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol))
        self.logger.debug('printed = %d' % self.printed_lines)
        if pminrow >= 0 and pminrow < self.printed_lines:
            self.timeline_win.refresh(pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol)


    def print_tweets(self, time_column_width, username_column_width, tweets):
        first_column_width = time_column_width + username_column_width + 2
        printed_lines = 0
        for tweet in tweets:
            self.timeline_win.addstr('%s %s | %s\n' % (tweet['time'], tweet['username'].rjust(username_column_width), tweet['tweet_lines'][0]))
            printed_lines = printed_lines + 1
            for line in tweet['tweet_lines'][1:]:
                self.timeline_win.addstr('%s %s\n' % ('|'.rjust(first_column_width), line))
                printed_lines = printed_lines + 1
        return printed_lines


class BarkTextbox(Textbox):
    def __init__(self, win, app):
        self.logger = Logger(__file__)
        self.app = app
        super().__init__(win)

    def do_command(self, ch):
        if ch == 338:
            self.app.do_page_down()
            return True
        elif ch == 339:
            self.app.do_page_up()
            return True
        else:
            return super().do_command(ch)
