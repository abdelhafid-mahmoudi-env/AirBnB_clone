#!/usr/bin/python3
"""Ce module définit des tests pour l'utilisateur"""

import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.user import User


class TestUser(unittest.TestCase):
    """
    Cette classe effectue des tests sur l'utilisateur
    """

    def setUp(self):
        """
        Cette méthode configure toutes les instances nécessaires pour les tests
        """
        self.storage = FileStorage()
        self.user = User()
        self.user.first_name = "John"
        self.user.last_name = "Doe"
        self.user.email = "john.doe@example.com"
        self.user.password = "password"
        self.storage.new(self.user)
        self.storage.save()

    def tearDown(self):
        """
        Cette méthode supprime le fichier json qui a été ouvert pour les tests
        """
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_user_instance(self):
        """Ce test vérifie l'instance de l'utilisateur"""
        self.assertIsInstance(self.user, User)

    def test_user_attributes(self):
        """Ce test vérifie les attributs de l'utilisateur"""
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.email, "john.doe@example.com")
        self.assertEqual(self.user.password, "password")


if __name__ == '__main__':
    unittest.main()
