#!/usr/bin/python3
import uuid
from datetime import datetime

class BaseModel:
    """
    Defines all common attributes/methods for other classes in the AirBnB clone project.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)
            self.id = kwargs.get('id', str(uuid.uuid4()))
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Updates the 'updated_at' attribute with the current datetime.
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of the instance's __dict__.
        This dictionary representation includes the class name under a '__class__' key,
        and the 'created_at' and 'updated_at' values are converted to strings in ISO format.
        """
        model_dict = self.__dict__.copy()
        model_dict['__class__'] = self.__class__.__name__
        model_dict['created_at'] = model_dict['created_at'].isoformat()
        model_dict['updated_at'] = model_dict['updated_at'].isoformat()
        return model_dict
