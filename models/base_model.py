#!/usr/bin/env python3
"""
Defines the BaseModel class that serves as a base for all other classes
in the AirBnB clone project.
"""

import uuid
from datetime import datetime


class BaseModel:
    """
    Defines all common attributes/methods for other classes.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new BaseModel instance.
        """
        self.id = str(uuid.uuid4())
        self.created_at = self.updated_at = datetime.now()
        for key, value in kwargs.items():
            if key == '__class__':
                continue
            if key in ['created_at', 'updated_at']:
                value = datetime.fromisoformat(value)
            setattr(self, key, value)

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.
        """
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """
        Updates the public instance attribute 'updated_at' with the current datetime.
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of the instance.
        """
        dictionary = dict(self.__dict__)
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
