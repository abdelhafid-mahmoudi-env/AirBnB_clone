#!/usr/bin/python3
""" Ce module définit des tests pour la ville """

import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.city import City


class TestCity(unittest.TestCase):
    """
    Cette classe effectue des tests sur la ville
    """

    def setUp(self):
        """
        Cette méthode configure toutes les instances nécessaires pour les tests
        """
        self.storage = FileStorage()
        self.city = City()
        self.city.name = "TestCity"
        self.city.state_id = "TestStateID"
        self.storage.new(self.city)
        self.storage.save()

    def tearDown(self):
        """
        Cette méthode supprime le fichier json qui a été ouvert pour les tests
        """
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_city_instance(self):
        """ Ce test vérifie l'instance de la ville """
        self.assertIsInstance(self.city, City)

    def test_city_attributes(self):
        """ Ce test vérifie les attributs de la ville """
        self.assertEqual(self.city.name, "TestCity")
        self.assertEqual(self.city.state_id, "TestStateID")


if __name__ == '__main__':
    unittest.main()
