import shutil
import curses

class PromptWidget:

    def __init__(self, username, begin_y, begin_x):
        terminal_size = shutil.get_terminal_size()
        self.terminal_width = terminal_size[0]
        self.terminal_height = terminal_size[1]
        self.prompt_width = len(username)+4
        self.prompt_win = curses.newwin(1, self.prompt_width, begin_y, begin_x)
        self.prompt_text = '[@'+username+']'
        self.prompt_win.addstr(self.prompt_text)
