import curses
import shutil

class StatusWidget:

    def __init__(self, begin_y, begin_x):
        terminal_size = shutil.get_terminal_size()
        self.terminal_width = terminal_size[0]
        self.terminal_height = terminal_size[1]
        self.status_win = curses.newwin(2, self.terminal_width, begin_y, begin_x)

    def set_status_text(self, status_text):
        self.status_win.addstr(0, 0, "-" * self.terminal_width)
        self.status_win.addstr(1, 0, status_text)
        return status_text
