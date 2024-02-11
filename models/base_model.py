#!/usr/bin/python3
"""
Defines the BaseModel class that serves as a base for all other classes
in our project.
"""
import uuid
from datetime import datetime


class BaseModel:
    """
    The BaseModel class from which future classes will be derived.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key in ['created_at', 'updated_at']:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != '__class__':
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
            from models import storage
            storage.new(self)

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Updates 'updated_at' with the current datetime, and saves the instance
        to the file storage.
        """
        self.updated_at = datetime.now()
        from models import storage
        storage.new(self)
        storage.save()

    def to_dict(self):
        """
        Returns a dictionary of the instance's __dict__, with objects
        converted to appropriate representation for JSON serialization,
        including the class name in the '__class__' key.
        """
        my_dict = dict(self.__dict__)
        my_dict['__class__'] = self.__class__.__name__
        my_dict['created_at'] = self.created_at.isoformat()
        my_dict['updated_at'] = self.updated_at.isoformat()
        return my_dict
