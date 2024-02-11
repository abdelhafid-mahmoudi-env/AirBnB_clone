#!/usr/bin/python3
"""BaseModel module: Defines all common"""

import uuid
from datetime import datetime


class BaseModel:
    """Defines all common attributes/methods for other classes."""

    def __init__(self, *args, **kwargs):
        """Initializes a new instance of BaseModel."""
        from models import storage
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ('created_at', 'updated_at'):
                        value = datetime.fromisoformat(value)
                    setattr(self, key, value)
            storage.new(self)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
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
        my_dict = {
            key: value.isoformat()
            if isinstance(value, datetime)
            else value for key, value in self.__dict__.items()
        }
        my_dict['__class__'] = self.__class__.__name__
        return my_dict
