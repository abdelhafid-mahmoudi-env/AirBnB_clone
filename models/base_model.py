#!/usr/bin/python3

from uuid import uuid4
from datetime import datetime
from models import storage


class BaseModel:
    """Defines all common attributes/methods for other classes."""

    def __init__(self, *args, **kwargs):
        """Initializes a new instance of BaseModel."""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key not in ('created_at', 'updated_at'):
                        setattr(self, key, value)
                    else:
                        setattr(self, key, datetime.fromisoformat(value))
        else:
            self.id = str(uuid4())
            self.created_at = self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """String representation of the BaseModel class."""
        return "[{}] ({}) {}".format(
                self.__class__.__name__,
                self.id,
                self.__dict__
            )

    def save(self):
        """Updates 'updated_at' with the current datetime."""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values."""
        temp_dict = {}
        for key, value in self.__dict__.items():
            temp_dict[key] = value if key not in ["created_at", "updated_at"]\
                else self.__getattribute__(key).isoformat()
        temp_dict['__class__'] = type(self).__name__
        return temp_dict
