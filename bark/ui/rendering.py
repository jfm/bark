import datetime
from bark.util.logger import Logger

class Render:

    def __init__(self):
        self.logger = Logger(__file__)

    def render_tweet(self, status, text_width):
        tweet = {}
        tweet['id'] = status.id
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
        text = text.replace('\n', ' ')
        if len(text) < text_width:
            result = []
            result.append(text)
            return result
        else:
            return self._break_up_text(text, text_width)

    def get_longest_username(self, usernames):
        longest_username = max(usernames, key=len)
        return len(longest_username)

    def _break_up_text(self, text, width):
        words = text.split()
        line = ""
        lines = []
        for word in words:
            if len(line + word) >= width-1:
                lines.append(line)
                line = word + " "
            else:
                line += word + " "
        lines.append(line)

        return lines
