#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
import ast


def parse_arguments(argument_line: str):
    """Parse command arguments to handle different types of inputs including JSON."""
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

    def default(self, line: str):
        """Handle unrecognized commands and custom syntax, including dot notation."""
        # Check if the command uses the dot notation for classes (e.g., User.update(...))
        dot_notation_match = re.match(r"(\w+)\.(\w+)\((.*)\)$", line)
        if dot_notation_match:
            class_name, method_name, arguments = dot_notation_match.groups()
            if class_name in self.supported_classes and hasattr(self, f"do_{method_name}"):
                # Prepare arguments, handling dictionaries specially
                if arguments.startswith("{"):
                    try:
                        # Safely evaluate dictionary arguments
                        arguments_dict = ast.literal_eval(arguments)
                        # Convert the dictionary back to a string for passing to the command method
                        arguments = f'"{class_name}" {str(arguments_dict)}'
                    except ValueError as e:
                        print(f"Error parsing dictionary: {e}")
                        return
                else:
                    arguments = f'"{class_name}" {arguments}'
                # Call the corresponding method with the parsed arguments
                getattr(self, f"do_{method_name}")(arguments)
            else:
                print(f"*** Unknown syntax: {line}")
        else:
            print(f"*** Unknown syntax: {line}")

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
        if len(arg_list) > 0 and arg_list[0] not in HBNBCommand.supported_classes:
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
        """Simplified do_update method focusing on best practices."""
        arg_list = parse_arguments(arg)
        if not self._validate_update_args(arg_list):
            return

        obj_key = "{}.{}".format(arg_list[0], arg_list[1])
        obj_dict = storage.all()
        if obj_key not in obj_dict:
            print("** no instance found **")
            return

        obj = obj_dict[obj_key]

        # Determine if the update argument is a dictionary
        if len(arg_list) == 3 and arg_list[2].startswith('{'):
            self._update_from_dict(obj, arg_list[2])
        elif len(arg_list) == 4:
            setattr(obj, arg_list[2], arg_list[3])
        else:
            print("** invalid arguments **")
            return

        obj.save()

    def _validate_update_args(self, args):
        """Validate the arguments passed to the update command."""
        if len(args) < 2:
            print("** class name missing **" if len(args) == 0 else "** instance id missing **")
            return False
        if args[0] not in self.supported_classes:
            print("** class doesn't exist **")
            return False
        if len(args) == 2:
            print("** attribute name missing **")
            return False
        if len(args) == 3 and not args[2].startswith('{'):
            print("** value missing **")
            return False
        return True

    def _update_from_dict(self, obj, dict_str):
        """Update the object from a dictionary string safely."""
        try:
            update_dict = ast.literal_eval(dict_str)
            if not isinstance(update_dict, dict):
                raise ValueError
            for key, value in update_dict.items():
                setattr(obj, key, value)
        except (ValueError, SyntaxError):
            print("** invalid dictionary format **")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
