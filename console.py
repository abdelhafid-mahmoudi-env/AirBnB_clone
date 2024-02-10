#!/usr/bin/python3
"""
Module for the HBNB (ALX School AirBnB clone) command interpreter.
"""

import cmd
from models import storage


class HBNBCommand(cmd.Cmd):
    """
    A command line interpreter for HBNB that includes commands
    to manage the application's data.
    """

    prompt = "(hbnb) "
    my_models = [
        "BaseModel",
        "User",
        "Place",
        "State",
        "City",
        "Amenity",
        "Review"
    ]

    def do_quit(self, args):
        """Exits the console."""
        return True

    def do_EOF(self, args):
        """Exits the console when receiving the EOF signal (Ctrl+D)."""
        return True

    def emptyline(self):
        """Does nothing upon receiving an empty line."""
        pass

    def do_create(self, args):
        """
        Creates a new instance of a given class
        Syntax: create <ClassName>
        """
        if args == "":
            print("** class name missing **")
        elif args not in HBNBCommand.my_models:
            print("** class doesn't exist **")
        else:
            a = eval(args)()
            print(a.id)
            a.save()

    def do_show(self, args):
        """
        Prints the string representation of an instance
        Syntax: show <ClassName> <id>
        """
        sw = 0
        arg = args.split()
        if args == "":
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.my_models:
            print("** class doesn't exist **")
        elif len(arg) < 2:
            print("** instance id missing **")
        else:
            in_key = arg[0] + "." + arg[1]
            for key, obj in storage.all().items():
                if key == in_key:
                    print(obj)
                    sw = 1
            if sw == 0:
                print("** no instance found **")

    def do_destroy(self, args):
        """
        Deletes an instance based on its class name and ID
        Syntax: destroy <ClassName> <id>
        """
        sw = 0
        arg = args.split()
        if args == "":
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.my_models:
            print("** class doesn't exist **")
        elif len(arg) < 2:
            print("** instance id missing **")
        else:
            in_key = arg[0] + "." + arg[1]
            dict_objects = storage.all()
            for key, obj in dict_objects.items():
                if key == in_key:
                    del dict_objects[key]
                    sw = 1
                    storage.save()
                    storage.reload()
                    return
            if sw == 0:
                print("** no instance found **")

    def do_count(self, args):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        arg = args.split()
        count = 0
        for obj in storage.all().values():
            if arg[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_all(self, args):
        """
        Prints all instances of a class
        Syntax: all <ClassName>
        """
        arg = args.split()
        list_ = []
        if arg[0] == "":
            for key, obj in storage.all().items():
                list_.append(str(obj))
            print(list_)
        elif arg[0].strip() in HBNBCommand.my_models:
            for key, obj in storage.all().items():
                if arg[0] == key.split(".")[0]:
                    list_.append(str(obj))
            print(list_)
        else:
            print("** class doesn't exist **")

    def do_update(self, args):
        """
        Updates an instance by adding or updating
        """
        arg = args.split()
        sw = 0
        if len(arg) < 1:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.my_models:
            print("** class doesn't exist **")
        elif len(arg) < 2:
            print("** instance id missing **")
        elif len(arg) < 3:
            print("** attribute name missing **")
        elif len(arg) < 4:
            print("** value missing **")
        else:
            in_key = arg[0] + "." + arg[1]
            for key, obj in storage.all().items():
                if key == in_key:
                    idx_arg = len(arg[0]) + len(arg[1]) + len(arg[2]) + 3
                    value = args[idx_arg:]
                    if args[idx_arg] == '"':
                        idx_arg += 1
                        value = args[idx_arg:-1]
                    if hasattr(obj, arg[2]):
                        value = type(getattr(obj, arg[2]))(args[idx_arg:])
                    setattr(obj, arg[2], value)
                    sw = 1
                    storage.save()
            if sw == 0:
                print("** no instance found **")
                return -1

    def default(self, args):
        """Handle unrecognized commands with custom patterns."""
        class_name, command, params = self.parse_custom_command(args)
        if class_name and command:
            self.execute_custom_command(class_name, command, params)
        else:
            print(f"** Command `{args}` not found **")

    def parse_custom_command(self, command):
        """Parse custom commands into components."""
        try:
            cls_cmd, params = command.split(".", 1)
            cmd, args = params.split("(", 1)
            args = args[:-1]  # Strip closing parenthesis
            return cls_cmd, cmd, args.replace('"', "").split(",")
        except ValueError:
            return None, None, None

    def execute_custom_command(self, cls, cmd, params):
        """Execute custom parsed commands."""

        if cls not in self.my_models:
            print("** class doesn't exist **")
            return

        method_name = f"do_{cmd}"
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method(" ".join([cls] + params))
        else:
            print(f"** Method {cmd} not available for {cls} **")


if __name__ == "__main__":
    comand = HBNBCommand()
    comand.cmdloop()
