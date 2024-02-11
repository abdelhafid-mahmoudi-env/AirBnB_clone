#!/usr/bin/python3
import unittest
from models.base_model import BaseModel
from datetime import datetime

class TestBaseModel(unittest.TestCase):
    """Définit des cas de test pour la classe BaseModel"""

    def test_id_creation(self):
        """Teste si un id est créé pour une nouvelle instance"""
        my_model = BaseModel()
        self.assertTrue(hasattr(my_model, "id"))

    def test_id_uniqueness(self):
        """Teste si chaque nouvelle instance a un id unique"""
        model1 = BaseModel()
        model2 = BaseModel()
        self.assertNotEqual(model1.id, model2.id)

    def test_created_at_assignment(self):
        """Teste si created_at est assigné pour une nouvelle instance"""
        my_model = BaseModel()
        self.assertTrue(hasattr(my_model, "created_at"))
        self.assertIsInstance(my_model.created_at, datetime)

    def test_updated_at_assignment(self):
        """Teste si updated_at est assigné pour une nouvelle instance"""
        my_model = BaseModel()
        self.assertTrue(hasattr(my_model, "updated_at"))
        self.assertIsInstance(my_model.updated_at, datetime)

    def test_to_dict(self):
        """Teste la méthode to_dict"""
        my_model = BaseModel()
        my_model.name = "My First Model"
        my_model.my_number = 89
        model_dict = my_model.to_dict()
        self.assertEqual(model_dict['name'], "My First Model")
        self.assertEqual(model_dict['my_number'], 89)
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertTrue('created_at' in model_dict)
        self.assertTrue('updated_at' in model_dict)

    def test_new_instance_from_dict(self):
        """Teste la création d'une nouvelle instance à partir d'un dictionnaire"""
        my_model = BaseModel()
        my_model_json = my_model.to_dict()
        my_new_model = BaseModel(**my_model_json)
        self.assertEqual(my_model.id, my_new_model.id)
        self.assertTrue(isinstance(my_new_model.created_at, datetime))
        self.assertFalse(my_model is my_new_model)

if __name__ == '__main__':
    unittest.main()
