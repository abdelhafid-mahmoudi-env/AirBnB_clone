#!/usr/bin/python3
"""
Serializes instances to a JSON file & deserializes JSON file to instances
"""
import json
from models.base_model import BaseModel


class FileStorage:
    """
    serializes instances to a JSON file and deserializes JSON file to instances
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Returns the dictionary '__objects'
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Sets in '__objects' the obj with key <obj class name>.id
        """
        if obj:
            key = obj.__class__.__name__ + '.' + obj.id
            self.__objects[key] = obj

    def save(self):
        """
        Serializes '__objects' to the JSON file (path: '__file_path')
        """
        obj_dict = {}
        for obj in self.__objects.keys():
            obj_dict[obj] = self.__objects[obj].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(obj_dict, f, indent=4)

    def reload(self):
        """
        Deserializes JSON file to '__objects'
        (only if the JSON file ('__file_path') exists;
        otherwise, do nothing. If the file doesn’t exist,
        no exception should be raised)
        """
        try:
            with open(self.__file_path, 'r') as f:
                obj_dict = json.load(f)
            for obj in obj_dict.values():
                class_name = obj['__class__']
                del obj['__class__']
                self.new(eval(class_name)(**obj))
        except FileNotFoundError:
            pass
