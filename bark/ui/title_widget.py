import shutil
import curses

class TitleWidget:
    def __init__(self, title_text, begin_y, begin_x):
        terminal_size = shutil.get_terminal_size()
        self.terminal_width = terminal_size[0]
        self.terminal_height = terminal_size[1]
        self.title_win = curses.newwin(1, self.terminal_width, begin_y, begin_x)
        self.set_title(title_text)
    
    def set_title(self, title_text):
        self.title_win.clear()
        if len(title_text) > self.terminal_width:
            title_text = title_text[:self.terminal_width-4] + '...'
        
        self.title_win.addstr(title_text)
        return title_text
