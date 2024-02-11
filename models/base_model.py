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
        Initializes a new instance of BaseModel.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

        for key, value in kwargs.items():
            if key != '__class__':
                if key in ('created_at', 'updated_at'):
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Updates the updated_at attribute with the current datetime.
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of the instance.
        """
        dict_rep = self.__dict__.copy()
        dict_rep['__class__'] = self.__class__.__name__
        dict_rep['created_at'] = self.created_at.isoformat()
        dict_rep['updated_at'] = self.updated_at.isoformat()
        return dict_rep
