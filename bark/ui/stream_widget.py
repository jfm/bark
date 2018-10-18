import curses
import shutil
from bark.util.logger import BarkLogger
from bark.ui.rendering import Render

class StreamWidget:

    def __init__(self, begin_y, begin_x):
       self.logger = BarkLogger(__file__)
       terminal_size = shutil.get_terminal_size()
       self.terminal_width = terminal_size[0]
       self.terminal_height = terminal_size[1]
       self.stream_pad =  curses.newpad(2000, self.terminal_width)
       self.tweets = []
       self.renderer = Render()
  
    def refresh_stream(self, time_line_statuses):
        index_column_width = 6
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
        text_column_width = self.terminal_width - index_column_width - username_column_width - 12

        #Build the rendered tweet objects
        for status in reversed(time_line_statuses):
            tweet = self.renderer.render_tweet(status, text_column_width)
            self.tweets.append(tweet)
            self.progress = tweet['id']

        self.stream_pad.clear()
        self.printed_lines = self.print_tweets(index_column_width, time_column_width, username_column_width, self.tweets)
        self.scroll_to(self.printed_lines-(self.terminal_height) + 4)
        return self.tweets

    def scroll_to(self, row):
        self.scroll_current = row
        pminrow = self.scroll_current
        pmincol = 0
        sminrow = 1
        smincol = 0
        smaxrow = self.terminal_height - 4
        smaxcol = self.terminal_width
        self.logger.debug('PAD REFRESH: pminrow = %d, pmincol = %d, sminrow = %d, smincol = %d, smaxrow = %d, smaxcol = %d' % (pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol))
        self.logger.debug('printed = %d' % self.printed_lines)
        if pminrow >= 0 and pminrow < self.printed_lines:
            self.stream_pad.refresh(pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol)


    def print_tweets(self, index_column_width, time_column_width, username_column_width, tweets):
        first_column_width = index_column_width + time_column_width + username_column_width + 2
        printed_lines = 0
        for index,tweet in enumerate(tweets):
            self.stream_pad.addstr('[%03d] %s %s | %s\n' % (index, tweet['time'], tweet['username'].rjust(username_column_width), tweet['tweet_lines'][0]))
            printed_lines = printed_lines + 1
            for line in tweet['tweet_lines'][1:]:
                self.stream_pad.addstr('%s %s\n' % ('|'.rjust(first_column_width), line))
                printed_lines = printed_lines + 1
        return printed_lines
