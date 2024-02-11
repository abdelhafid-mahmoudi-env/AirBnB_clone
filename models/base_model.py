#!/usr/bin/python3

from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Defines all common attributes/methods for other classes."""

    def __init__(self, *args, **kwargs):
        """Initializes a new instance of BaseModel."""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs and (kwargs is not None) and (kwargs != {}):
            for attr, value in kwargs.items():
                if attr == "__class__":
                    continue
                elif attr == "created_at" or attr == "updated_at":
                    new_attr_value = datetime.fromisoformat(kwargs[attr])
                    setattr(self, attr, new_attr_value)
                else:
                    setattr(self, attr, value)
            storage.new(self)
        else:
            from models import storage
            storage.new(self)

    def __str__(self):
        """String representation of the BaseModel class."""
        return "[{}] ({}) {}".format(
                self.__class__.__name__,
                self.id,
                self.__dict__
            )

    def __repr__(self):
        """
        returns string repr
        """
        return (self.__str__())

    def save(self):
        """Updates 'updated_at' with the current datetime."""
        self.updated_at = datetime.now()
        from models import storage
        storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values."""
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = my_dict["created_at"].isoformat()
        my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        return my_dict
