import datetime
from cmd import Cmd

class TwitterPrompt(Cmd):

    def __init__(self, api):
        self.api = api
        self.renderer = Render()
        credentials = api.VerifyCredentials()
        self.prompt = '[%s] ' % credentials.screen_name
        self.do_refresh('')
        super().__init__()

    def do_refresh(self, line):
        time_line_statuses = self.api.GetHomeTimeline()
        length_longest_username = self.renderer.get_longest_username(time_line_statuses)
        for status in reversed(time_line_statuses):
            self.renderer.render_tweet(status.created_at, status.user.screen_name, status.text, length_longest_username)

    def do_tweet(self, line):
        #self.api.PostUpdate(line)
        print('Would have Tweeted: %s' % line)

    def do_exit(self, line):
        return True

    def EOF(self, line):
        return True

class Render:
    def render_tweet(self, created_at, username, text, username_length):
        rendered_time = self.render_time(created_at)
        rendered_username = self.render_username(username, username_length)
        rendered_tweet = self.render_text(text)
        print('%s %s | %s' % (rendered_time, rendered_username, rendered_tweet))

    def render_time(self, created_at):
        timestamp = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
        return timestamp.strftime('%H:%M:%S')

    def render_username(self, username, length):
        return username.rjust(length)

    def render_text(self, text):
        return text

    def get_longest_username(self, statuses):
        usernames = []
        for status in statuses:
            usernames.append(status.user.screen_name)
        longest_username = max(usernames, key=len)
        return len(longest_username)
