#!/usr/bin/python3
"""
This module contains the entry point of the command interpreter.
"""

import cmd


class HBNBCommand(cmd.Cmd):
    """
    This class defines the command interpreter for the HBNB console.
    """

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """
        Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """
        Exit the program cleanly using EOF (Ctrl+D)
        """
        return True

    def emptyline(self):
        """
        Do nothing on empty input line
        """
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
