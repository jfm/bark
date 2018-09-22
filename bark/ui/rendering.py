import logging
import datetime

class Render:

    def __init__(self):
        self.logger = logging.getLogger(__file__)
        hdlr = logging.FileHandler(__file__ + ".log")
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)

    def render_tweet(self, status, text_width):
        tweet = {}
        tweet['time'] = self.render_time(status.created_at)
        tweet['username'] = self.render_username(status.user.screen_name)
        tweet['tweet_lines'] = self.render_text(status.text, text_width)
        return tweet

    def render_time(self, created_at):
        timestamp = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
        return timestamp.strftime('%H:%M:%S')

    def render_username(self, username):
        return username

    def render_text(self, text, text_width):
        if len(text) < text_width:
            result = []
            result.append(text)
            return result
        else:
            return self._break_up_text(text, text_width)

    def get_longest_username(self, statuses):
        usernames = []
        for status in statuses:
            usernames.append(status.user.screen_name)
        longest_username = max(usernames, key=len)
        return len(longest_username)

    def _break_up_text(self, text, width):
        words = text.split()
        line = ""
        lines = []
        for word in words:
            self.logger.debug(word)
            if len(line + word) >= width-1:
                lines.append(line)
                line = word + " "
            else:
                line += word + " "
        lines.append(line)

        return lines
