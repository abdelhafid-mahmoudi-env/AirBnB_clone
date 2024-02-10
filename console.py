#!/usr/bin/python3
"""
This module contains the entry point of the command interpreter.
"""

import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import models
import json


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

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves it, and prints the id.
        Usage: create <class name>
        """
        if not arg:
            print("** class name missing **")
        elif arg not in {'BaseModel'}:
            print("** class doesn't exist **")
        else:
            new_instance = BaseModel()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance.
        Usage: show <class name> <id>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in {'BaseModel'}:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            objs = storage.all()
            key = args[0] + '.' + args[1]
            if key not in objs:
                print("** no instance found **")
            else:
                print(objs[key])

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id.
        Usage: destroy <class name> <id>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in {'BaseModel'}:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            objs = storage.all()
            key = args[0] + '.' + args[1]
            if key not in objs:
                print("** no instance found **")
            else:
                del objs[key]
                storage.save()

    def do_all(self, arg):
        """
        Prints all string representation of all instances.
        Usage: all [<class name>]
        """
        args = arg.split()
        objs = storage.all()
        if not args:
            print([str(objs[obj]) for obj in objs])
        elif args[0] not in {'BaseModel'}:
            print("** class doesn't exist **")
        else:
            prefix = args[0] + '.'
            print([str(objs[obj]) for obj in objs if obj.startswith(prefix)])

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id.
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in {'BaseModel'}:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            objs = storage.all()
            key = args[0] + '.' + args[1]
            if key not in objs:
                print("** no instance found **")
            else:
                setattr(objs[key], args[2], args[3].strip('"'))
                objs[key].save()

    def do_count(self, arg):
        """
        Count the number of instances of a class.
        """
        class_name = arg
        count = 0
        if class_name in storage.classes():  # Assuming storage.classes() returns a list of valid class names
            for obj in storage.all().values():  # Assuming storage.all() returns a dict of all objects
                if obj.__class__.__name__ == class_name:
                    count += 1
            print(count)
        else:
            print("** class doesn't exist **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
