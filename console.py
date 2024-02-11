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
from datetime import datetime


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

    SHOW = r'^(\w+)\.show(\("([^"]+)"\))?$'
    DESTROY = r'^(\w+)\.destroy\("([^"]+)"\)$'
    UPDATE_ATTR = r'^(\w+)\.update\("([^"]+)", "([^"]+)", ("[^"]+"|\d+)\)$'
    UPDATE_DICT = r'^(\w+)\.update\("([^"]+)", (\{.*\})\)$'

    def default(self, line):
        """Handle unrecognized commands."""
        parts = line.split('.')
        if len(parts) == 2:
            if parts[1] == "all()":
                self.do_all(parts[0])
            elif parts[1] == "count()":
                self.do_count(parts[0])
            elif re.match(HBNBCommand.SHOW, line):
                match = re.match(HBNBCommand.SHOW, line)
                self.do_show(f"{match.group(1)} {match.group(2)}")
            elif re.match(HBNBCommand.DESTROY, line):
                match = re.match(HBNBCommand.DESTROY, line)
                self.do_destroy(f"{match.group(1)} {match.group(2)}")
            elif re.match(HBNBCommand.UPDATE_ATTR, line):
                match = re.match(HBNBCommand.UPDATE_ATTR, line)
                class_name, obj_id, attr_name, attr_val = match.groups()
                self.do_update(f'{class_name} {obj_id} {attr_name} {attr_val}')
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
            else:
                print("** class doesn't exist **")
                return
        else:
            cmd.Cmd.default(self, line)

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

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

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

    def do_update(self, arg):
        """Updates an instance based on the class name and id."""
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
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print("** value missing **")
            return
        all_objs = storage.all()
        key = args[0] + '.' + args[1]
        if key not in all_objs:
            print("** no instance found **")
            return
        obj = all_objs[key]
        attr_name = args[2]
        attr_val = args[3].strip('"')
        if attr_val.isdigit():
            attr_val = int(attr_val)
        else:
            try:
                attr_val = float(attr_val)
            except ValueError:
                pass
        setattr(obj, attr_name, attr_val)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
