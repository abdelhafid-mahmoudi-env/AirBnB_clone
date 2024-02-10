import json
import os
from typing import Dict, Type, Any

from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """FileStorage class with dynamic attribute retrieval."""

    __file_path = "file.json"
    __objects: Dict[str, BaseModel] = {}

    def all(self) -> Dict[str, BaseModel]:
        """Returns the dictionary of all objects."""
        return self.__objects

    def new(self, obj: BaseModel) -> None:
        """Adds a new object to the storage."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self) -> None:
        """Saves all objects to the JSON file."""
        obj_dict = {
            obj_id: obj.to_dict()
            for obj_id, obj in self.__objects.items()
        }
        with open(self.__file_path, 'w') as f:
            json.dump(obj_dict, f)

    def reload(self) -> None:
        """Reloads objects from the JSON file, if it exists."""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as f:
                obj_dict = json.load(f)
            for obj_id, obj_data in obj_dict.items():
                cls_name = obj_data['__class__']
                cls = self.classes().get(cls_name)
                if cls:
                    self.__objects[obj_id] = cls(**obj_data)

    def classes(self) -> Dict[str, Type[BaseModel]]:
        """Returns a dictionary of valid classes."""
        return {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review,
        }
