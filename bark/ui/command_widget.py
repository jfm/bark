import shutil
import curses

class CommandWidget:

    def __init__(self, begin_y, begin_x):
        terminal_size = shutil.get_terminal_size()
        self.terminal_width = terminal_size[0]
        self.terminal_height = terminal_size[1]
        self.command_win = curses.newwin(1, self.terminal_width, begin_y, begin_x)
        self.command_box = Textbox(command_win, self)
        self.command_box.stripspaces = 1

    def get_command(self, validation_method):
        command = self.command_box.edit(validate=validation_method)
        self.command_win.clear()
        return command
