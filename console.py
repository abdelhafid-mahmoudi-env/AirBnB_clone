#!/usr/bin/python3
import cmd
from models import storage
from models.base_model import BaseModel

class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """End of file condition to exit the program"""
        print()
        return True

    def emptyline(self):
        """Do nothing upon receiving an empty line"""
        pass

    # Add other commands here

if __name__ == '__main__':
    HBNBCommand().cmdloop()

