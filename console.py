#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage


def parse_arguments(argument_line: str):
    """Parse command arguments to handle different types of inputs."""
    curly_braces_match = re.search(r"\{(.*?)\}", argument_line)
    brackets_match = re.search(r"\[(.*?)\]", argument_line)

    if curly_braces_match:
        arguments_part = argument_line[: curly_braces_match.span()[0]]
    elif brackets_match:
        arguments_part = argument_line[: brackets_match.span()[0]]
    else:
        arguments_part = argument_line

    parsed_arguments = [arg.strip(",") for arg in split(arguments_part)]

    if curly_braces_match:
        parsed_arguments.append(curly_braces_match.group())
    elif brackets_match:
        parsed_arguments.append(brackets_match.group())

    return parsed_arguments


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    supported_classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review",
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, line: str) -> bool:
        """Handles unrecognized commands."""
        action, _, params = line.partition(".")
        if action in self.supported_classes:
            command, args = self._extract_command_and_args(params)
            if command in self._get_command_mappings():
                self._execute_command(action, command, args)
                return  # Prevent exit
        print(f"*** Unknown syntax: {line}")
        return False

    def _extract_command_and_args(self, params: str):
        """Extracts the command name and its arguments from params."""
        command_match = re.match(r"(\w+)\((.*)\)", params)
        if command_match:
            return command_match.group(1), command_match.group(2).strip('"')
        return "", ""

    def _execute_command(self, class_name: str, command: str, args: str):
        """Executes a specific command based on the parsed input."""
        action = self._get_command_mappings().get(command)
        if action:
            arg_line = f"{class_name} {args}" if args else class_name
            action(arg_line)
            return True
        return False

    def _get_command_mappings(self):
        """Returns a mapping of commands to their corresponding methods."""
        return {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update,
        }

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        arg_list = parse_arguments(arg)
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.supported_classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg_list[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        arg_list = parse_arguments(arg)
        obj_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.supported_classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(arg_list[0], arg_list[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        arg_list = parse_arguments(arg)
        obj_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.supported_classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        arg_list = parse_arguments(arg)
        supported = HBNBCommand.supported_classes
        if len(arg_list) > 0 and arg_list[0] not in supported:
            print("** class doesn't exist **")
        else:
            obj_list = []
            for obj in storage.all().values():
                if len(arg_list) > 0 and arg_list[0] == obj.__class__.__name__:
                    obj_list.append(obj.__str__())
                elif len(arg_list) == 0:
                    obj_list.append(obj.__str__())
            print(obj_list)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        arg_list = parse_arguments(arg)
        count = 0
        for obj in storage.all().values():
            if arg_list[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
        <class>.update(<id>, <attribute_name>, <attribute_value>) or
        <class>.update(<id>, <dictionary>)
         Update a class instance of a given id by adding or updating
         a given attribute key/value pair or dictionary."""
        arg_list = parse_arguments(arg)
        obj_dict = storage.all()

        if len(arg_list) == 0:
            print("** class name missing **")
            return False
        if arg_list[0] not in HBNBCommand.supported_classes:
            print("** class doesn't exist **")
            return False
        if len(arg_list) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(arg_list) == 2:
            print("** attribute name missing **")
            return False
        if len(arg_list) == 3:
            try:
                type(eval(arg_list[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arg_list) == 4:
            obj = obj_dict
            obj = obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            if arg_list[2] in obj.__class__.__dict__.keys():
                val_type = type(obj.__class__.__dict__[arg_list[2]])
                obj.__dict__[arg_list[2]] = val_type(arg_list[3])
            else:
                obj.__dict__[arg_list[2]] = arg_list[3]
        elif type(eval(arg_list[2])) == dict:
            obj = obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            for key, value in eval(arg_list[2]).items():
                if key in obj.__class__.__dict__.keys() and type(
                    obj.__class__.__dict__[key]
                ) in {str, int, float}:
                    val_type = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = val_type(value)
                else:
                    obj.__dict__[key] = value
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
