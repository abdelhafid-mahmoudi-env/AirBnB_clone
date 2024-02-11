#!/usr/bin/python3
"""Ce module définit des tests pour l'examen"""

import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.review import Review


class TestReview(unittest.TestCase):
    """
    Cette classe effectue des tests sur l'examen
    """

    def setUp(self):
        """
        Cette méthode configure toutes les instances nécessaires pour les tests
        """
        self.storage = FileStorage()
        self.review = Review()
        self.review.text = "TestReview"
        self.storage.new(self.review)
        self.storage.save()

    def tearDown(self):
        """
        Cette méthode supprime le fichier json qui a été ouvert pour les tests
        """
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_review_instance(self):
        """Ce test vérifie l'instance de l'examen"""
        self.assertIsInstance(self.review, Review)

    def test_review_text(self):
        """Ce test vérifie le texte de l'examen"""
        self.assertEqual(self.review.text, "TestReview")


if __name__ == '__main__':
    unittest.main()
