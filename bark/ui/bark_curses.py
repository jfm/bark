import shutil
import curses
from curses.textpad import Textbox

class BarkCurses:

    def main(self, stdscr):
        terminal_size = shutil.get_terminal_size()
        terminal_width = terminal_size[0]
        terminal_height = terminal_size[1]
 
        # Clear screen
        stdscr.clear()
        
        self.timeline_win = self.create_timeline_win(terminal_height, terminal_width)
        
        prompt_win, prompt_width = self.create_prompt_win('jesperfusmoerk', terminal_height, terminal_width)
        prompt_win.refresh()
        
        edit_line_win = self.create_edit_line_win(terminal_height, terminal_width, prompt_width)
        box = Textbox(edit_line_win)
        box.stripspaces = 1
        while True:
            box.edit()
            message = box.gather()
            edit_line_win.clear()
            self.handle_command(message)

    def create_timeline_win(self, terminal_height, terminal_width):
        return curses.newwin(terminal_height-1, terminal_width, 0, 0)

    def create_prompt_win(self, username, terminal_height, terminal_width):
        prompt_width = len(username)+4
        prompt_win = curses.newwin(1, prompt_width, terminal_height-1, 0)
        prompt_win.addstr('[@'+username+']')
        return prompt_win, prompt_width

    def create_edit_line_win(self, terminal_height, terminal_width, prompt_width):
        win = curses.newwin(1, terminal_width, terminal_height-1, prompt_width)
        return win 
       
    def handle_command(self, message):
        stripped_message = message.strip()
        if stripped_message.lower() == "refresh":
            self.timeline_win.addstr(stripped_message)
            self.timeline_win.refresh()
 

if __name__ == '__main__':
    barkCurses = BarkCurses()
    curses.wrapper(barkCurses.main)
