#!/usr/bin/python3
"""
Defines the BaseModel class that serves as a base for all other classes
in our project.
"""
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """
    The BaseModel class from which future classes will be derived.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class.
        If kwargs is not empty, initializes with key-value pairs in kwargs,
        converting datetime strings to datetime objects for created_at and
        updated_at. Otherwise, initializes with a new UUID and the current
        datetime for created_at and updated_at.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.fromisoformat(value)
                if key != '__class__':
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.
        """
        cls_name = self.__class__.__name__
        return f"[{cls_name}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Updates 'updated_at' with the current datetime.
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Returns a dictionary of the instance's __dict__.
        """
        my_dict = self.__dict__.copy()
        my_dict['__class__'] = self.__class__.__name__
        my_dict['created_at'] = self.created_at.isoformat()
        my_dict['updated_at'] = self.updated_at.isoformat()
        return my_dict
