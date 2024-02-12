#!/usr/bin/python3
"""Ce module définit des tests pour le stockage de fichiers"""

import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):
    """
    Cette classe effectue des tests sur le stockage
    des fichiers de ce projet
    """

    def setUp(self):
        """
        Cette méthode configure toutes les instances nécessaires pour les tests
        """
        self.storage = FileStorage()
        self.base_model = BaseModel()
        self.base_model_dict = self.base_model.to_dict()
        self.storage.new(self.base_model)
        self.storage.save()

    def tearDown(self):
        """
        Cette méthode supprime le fichier json qui a été ouvert pour les tests
        """
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_json_file_exist(self):
        """Ce test vérifie l'existence du fichier json
        lors de la création d'une instance de la classe FileStorage"""
        self.assertTrue(os.path.exists(FileStorage._FileStorage__file_path))

    def test_all(self):
        """Test de la fonction "all" de la classe de stockage."""
        objects = self.storage.all()
        key = self.base_model.__class__.__name__ + "." + self.base_model.id
        self.assertTrue(isinstance(objects, dict))
        self.assertTrue(isinstance(objects[key], BaseModel))
        self.assertIn(key, objects)

    def test_new(self):
        """Test pour la nouvelle méthode"""
        new_model = BaseModel()
        self.storage.new(new_model)
        objects = self.storage.all()
        key = new_model.__class__.__name__ + "." + new_model.id
        self.assertIn(key, objects)
        self.assertTrue(isinstance(objects[key], BaseModel))

    def test_save_reload(self):
        """Test pour les méthodes save et reload"""
        self.storage.save()
        objects_before_reload = self.storage.all()
        self.storage.reload()
        objects_after_reload = self.storage.all()
        self.assertEqual(objects_before_reload, objects_after_reload)

    def test_json_file_content(self):
        """Tests pour le contenu du fichier json"""
        with open(FileStorage._FileStorage__file_path, 'r') as f:
            file_content = f.read()
            file_data = json.loads(file_content)
            self.assertIn(
                    self.base_model.__class__.__name__ +
                    "." + self.base_model.id, file_data
                    )


if __name__ == '__main__':
    unittest.main()
