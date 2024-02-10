#!/usr/bin/python3
import json
from models.base_model import BaseModel


class FileStorage:
    """Serializes instances to a JSON file and deserializes."""

    __file_path = "file.json"  # Path to the JSON file
    __objects = {}  # Dictionary to store all objects by <class name>.id

    def all(self):
        """Returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        obj_dict = {
                obj_id: obj.to_dict()
                for obj_id, obj in FileStorage.__objects.items()
        }
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects, if file exists."""
        try:
            with open(FileStorage.__file_path, 'r') as f:
                objs = json.load(f)
            for obj_id, obj_data in objs.items():
                cls_name = obj_data['__class__']
                cls = globals()[cls_name]
                FileStorage.__objects[obj_id] = cls(**obj_data)
        except FileNotFoundError:
            pass
