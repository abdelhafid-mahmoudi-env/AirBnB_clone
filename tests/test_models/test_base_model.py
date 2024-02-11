#!/usr/bin/python3
"""Unit Test for BaseModel"""

import unittest
from models.base_model import BaseModel
from datetime import datetime


class TestBaseModel(unittest.TestCase):
    """
    Test cases for the BaseModel class
    """

    def test_init(self):
        """
        Test initialization of BaseModel instance
        """
        model = BaseModel()
        self.assertTrue(hasattr(model, "id"))
        self.assertTrue(hasattr(model, "created_at"))
        self.assertTrue(hasattr(model, "updated_at"))
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    def test_str(self):
        """
        Test the __str__ method
        """
        model = BaseModel()
        expected = f"[BaseModel] ({model.id}) {model.__dict__}"
        self.assertEqual(model.__str__(), expected)

    def test_save(self):
        """
        Test the save method
        """
        model = BaseModel()
        old_updated_at = model.updated_at
        model.save()
        self.assertNotEqual(model.updated_at, old_updated_at)

    def test_to_dict(self):
        """
        Test the to_dict method
        """
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertEqual(model_dict['id'], model.id)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)

if __name__ == "__main__":
    unittest.main()
