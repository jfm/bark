import datetime
import shutil
from cmd import Cmd

class TwitterPrompt(Cmd):

    def __init__(self, api):
        terminal_size = shutil.get_terminal_size()
        self.terminal_width = terminal_size[0]
        self.terminal_height = terminal_size[1]
        self.api = api
        self.renderer = Render()
        credentials = api.VerifyCredentials()
        self.prompt = '[%s] ' % credentials.screen_name
        self.do_refresh('')
        super().__init__()

    def do_refresh(self, line):
        time_line_statuses = self.api.GetHomeTimeline()
        time_column_width = 9
        username_column_width = self.renderer.get_longest_username(time_line_statuses)
        text_column_width = self.terminal_width - username_column_width - 12
        for status in reversed(time_line_statuses):
            #print(status)
            self.renderer.render_tweet(status.created_at, status.user.screen_name, status.text, time_column_width, username_column_width, text_column_width)

    def do_tweet(self, line):
        #self.api.PostUpdate(line)
        print('Would have Tweeted: %s' % line)

    def do_exit(self, line):
        return True

    def EOF(self, line):
        return True

class Render:
    def render_tweet(self, created_at, username, text, time_width, username_width, text_width):
        rendered_time = self.render_time(created_at)
        rendered_username = self.render_username(username, username_width)
        rendered_tweet = self.render_text(text, text_width, time_width + username_width)
        print('%s %s | %s' % (rendered_time, rendered_username, rendered_tweet))

    def render_time(self, created_at):
        timestamp = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
        return timestamp.strftime('%H:%M:%S')

    def render_username(self, username, length):
        return username.rjust(length)

    def render_text(self, text, text_width, line_padding):
        if len(text) < text_width:
            return text
        else:
            return self._break_up_text(text, text_width, line_padding)

    def get_longest_username(self, statuses):
        usernames = []
        for status in statuses:
            usernames.append(status.user.screen_name)
        longest_username = max(usernames, key=len)
        return len(longest_username)

    def _break_up_text(self, text, width, padding):
        words = text.split()
        line = ''
        lines = []
        for word in words:
            if len(line + word) >= width:
                lines.append(line)
                line = word + ' '
            else:
                line += word + ' '
        lines.append(line)

        text_line = lines[0]
        for rline in lines[1:]:
            text_line = text_line + '\n' + '| '.rjust(padding + 3) + rline

        return text_line
