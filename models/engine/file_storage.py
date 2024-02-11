#!/usr/bin/python3
"""file serialization-deserialization"""

import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON."""
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """Returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        key = obj.__class__.__name__ + '.' + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        obj_dict = {}
        with open(self.__file_path, 'w', encoding="utf-8") as f:
            for k, v in FileStorage.__objects.items():
                obj_dict[k] = v.to_dict()
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects, if it exists."""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                obj_dict = json.load(f)
                for obj_id, obj_attrs in obj_dict.items():
                    cls_name = obj_attrs["__class__"]
                    cls = eval(cls_name)
                    FileStorage.__objects[obj_id] = cls(**obj_attrs)
        except FileNotFoundError:
            pass
