#!/usr/bin/python3

import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '
    class_list = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review,
    }

    SHOW = r'^(\w+)\.show(?:\((.*?)\))?$'
    DESTROY = r'^(\w+)\.destroy(?:\((.*?)\))?$'
    UPDATE_ATTR = r'^(\w+)\.update\("([^"]+)", "([^"]+)", ("[^"]+"|\d+)\)$'
    UPDATE_DICT = r'^(\w+)\.update\("([^"]+)", (\{.*\})\)$'

    def default(self, line):
        """Handle unrecognized commands."""
        parts = line.split('.')
        if len(parts) == 2:
            if parts[1] == "all()":
                self.do_all(parts[0])
                return
            elif parts[1] == "count()":
                self.do_count(parts[0])
                return
            elif re.match(HBNBCommand.SHOW, line):
                match = re.match(HBNBCommand.SHOW, line)
                self.do_show(f"{match.group(1)} {match.group(2)}")
                return
            elif re.match(HBNBCommand.DESTROY, line):
                match = re.match(HBNBCommand.DESTROY, line)
                self.do_destroy(f"{match.group(1)} {match.group(2)}")
                return
            elif re.match(HBNBCommand.UPDATE_ATTR, line):
                match = re.match(HBNBCommand.UPDATE_ATTR, line)
                class_name, obj_id, attr_name, attr_val = match.groups()
                self.do_update(f'{class_name} {obj_id} {attr_name} {attr_val}')
                return
            elif re.match(HBNBCommand.UPDATE_DICT, line):
                match = re.match(HBNBCommand.UPDATE_DICT, line)
                class_name, obj_id, dict_str = match.groups()
                try:
                    attr_dict = eval(dict_str)
                    if isinstance(attr_dict, dict):
                        for attr_name, attr_val in attr_dict.items():
                            cmd = (
                                f'{class_name} {obj_id} '
                                f'{attr_name} "{attr_val}"'
                            )
                            self.do_update(cmd)
                    else:
                        raise TypeError
                except Exception as e:
                    print("** invalid dictionary representation **")
                    return
                return
            else:
                print("** class doesn't exist **")
                return
        else:
            cmd.Cmd.default(self, line)
            return

    def do_count(self, class_name):
        """Counts the number of instances of a class."""
        if class_name not in self.class_list.keys():
            print("** class doesn't exist **")
            return
        count = 0
        for obj in storage.all().values():
            if obj.__class__.__name__ == class_name:
                count += 1
        print(count)

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def help_quit(self):
        """Help when quit is entered
        """
        print("Quit command to exit the program\n")

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def help_EOF(self):
        """Help when EOF is entered
        """
        print("EOF command to exit the program\n")

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel."""
        if not arg:
            print("** class name missing **")
            return
        if arg not in self.class_list:
            print("** class doesn't exist **")
            return
        instance = self.class_list[arg]()
        instance.save()
        print(instance.id)

    def help_create(self):
        """shows what create does
        """
        print("creates a new instance of a class")
        print("Usage: create <model_name>\n")

    def do_show(self, arg):
        """Prints the string representation."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.class_list:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        all_objs = storage.all()
        key = args[0] + '.' + args[1]
        if key not in all_objs:
            print("** no instance found **")
            return
        print(all_objs[key])

    def help_show(self):
        """shows what show does
        """
        print(
            "Prints the string representation" +
            " of an instance based on the class name and id")
        print("Usage: show <model_name> <id>\n")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.class_list:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        all_objs = storage.all()
        key = args[0] + '.' + args[1]
        if key in all_objs:
            del all_objs[key]
            storage.save()
        else:
            print("** no instance found **")

    def help_destroy(self):
        """shows what destroy does
        """
        print("Deletes an instance based on the class name and id")
        print("Usage: destroy <model_name> <id>\n")

    def do_all(self, arg):
        """Prints all string representation of all instances."""
        all_objs = storage.all()
        if arg:
            if arg not in self.class_list:
                print("** class doesn't exist **")
                return
            print([
                str(obj)
                for key, obj in all_objs.items()
                if type(obj).__name__ == arg
            ])
        else:
            print([str(obj) for obj in all_objs.values()])

    def help_all(self):
        """shows what all does
        """
        print("Prints all string representation" +
              " of all instances based or not on the class name")
        print("Usage: all [model_name]\n")

    def do_update(self, arg):
        """Updates an instance based on the class name and id
        by adding or updating attribute
        """
        args = arg.split()
        if not args or not args[0]:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.class_list.keys():
            print("** class doesn't exist **")
            return
        if len(args) < 2 or not args[1]:
            print("** instance id missing **")
            return
        id = args[1]
        all_objects = storage.all()
        key = f"{class_name}.{id}"
        if key not in all_objects.keys():
            print("** no instance found **")
            return
        if len(args) < 3 or not args[2]:
            print("** attribute name missing **")
            return
        if args[2] in ['id', 'created_at', 'updated_at']:
            print("** cannot update id, created_at, or updated_at **")
            return
        if len(args) < 4 or not args[3]:
            print("** value missing **")
            return
        value = args[3]
        if value[0] == '"':
            value = value[1:-1]
        float_value = False
        try:
            float_value = float(value)
            float_value = True
        except ValueError:
            float_value = False
        int_value = False
        try:
            int_value = int(value)
            int_value = True
        except ValueError:
            int_value = False
        if int_value:
            casted_arg = int(value)
        elif float_value:
            casted_arg = float(value)
        else:
            casted_arg = str(value)
        setattr(all_objects[key], args[2], casted_arg)
        storage.save()

    def help_update(self):
        """shows what update does"""
        print("Update an instance based on" +
              " the class name and id by adding or updating attribute")
        print('update <class name> <id> <attribute name>' +
              '"<attribute value>"\n')


if __name__ == '__main__':
    HBNBCommand().cmdloop()
