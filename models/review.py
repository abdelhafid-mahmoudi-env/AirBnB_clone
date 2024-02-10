#!/usr/bin/python3
"""Module containing the Review class"""

from models.base_model import BaseModel


class Review(BaseModel):
    """
    Review class that inherits from BaseModel.
    Attributes:
        place_id (str): The id of the place being reviewed.
        user_id (str): The id of the user who wrote the review.
        text (str): The text content of the review.
    """
    place_id = ""
    user_id = ""
    text = ""
