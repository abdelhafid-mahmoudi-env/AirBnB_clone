#!/usr/bin/python3
"""This module contains the file storage class"""
import os
import json


class FileStorage:
    """Serializes instances to JSON file and vice versa"""
    __file_path = "file.json"
    __objects = {}

    def __init__(self):
        """initializes objects with defined attributes"""
        pass

    def all(self):
        """returns a dicitonary of objects in `__objects`"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the `obj` with key <obj class name>.id"""
        key = obj.__class__.__name__ + "." + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes `__objects` to the JSON file"""
        obj_dict = {}
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            for k, v in FileStorage.__objects.items():
                obj_dict[k] = v.to_dict()
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes JSON to the `__objects`"""
        if not os.path.exists(FileStorage.__file_path):
            return
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            obj_dict = json.load(f)
            for k, v in obj_dict.items():
                obj_inst = eval(v["__class__"])(**v)
                FileStorage.__objects[k] = obj_inst
