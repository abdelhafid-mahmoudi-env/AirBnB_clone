#!/usr/bin/python3
"""Module containing the Amenity class"""

from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity class that inherits from BaseModel.
    Attributes:
        name (str): The name of the amenity.
    """
    name = ""
