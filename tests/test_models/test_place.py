#!/usr/bin/python3
"""Ce module définit des tests pour le lieu"""

import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.place import Place


class TestPlace(unittest.TestCase):
    """
    Cette classe effectue des tests sur le lieu
    """

    def setUp(self):
        """
        Cette méthode configure toutes les instances nécessaires pour les tests
        """
        self.storage = FileStorage()
        self.place = Place()
        self.place.city_id = "TestCityID"
        self.place.user_id = "TestUserID"
        self.place.name = "TestPlace"
        self.place.description = "TestDescription"
        self.place.number_rooms = 5
        self.place.number_bathrooms = 3
        self.place.max_guest = 10
        self.place.price_by_night = 100
        self.place.latitude = 40.7128
        self.place.longitude = -74.0060
        self.place.amenity_ids = ["1", "2", "3"]
        self.storage.new(self.place)
        self.storage.save()

    def tearDown(self):
        """
        Cette méthode supprime le fichier json qui a été ouvert pour les tests
        """
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_place_instance(self):
        """Ce test vérifie l'instance du lieu"""
        self.assertIsInstance(self.place, Place)

    def test_place_attributes(self):
        """Ce test vérifie les attributs du lieu"""
        self.assertEqual(self.place.city_id, "TestCityID")
        self.assertEqual(self.place.user_id, "TestUserID")
        self.assertEqual(self.place.name, "TestPlace")
        self.assertEqual(self.place.description, "TestDescription")
        self.assertEqual(self.place.number_rooms, 5)
        self.assertEqual(self.place.number_bathrooms, 3)
        self.assertEqual(self.place.max_guest, 10)
        self.assertEqual(self.place.price_by_night, 100)
        self.assertEqual(self.place.latitude, 40.7128)
        self.assertEqual(self.place.longitude, -74.0060)
        self.assertEqual(self.place.amenity_ids, ["1", "2", "3"])


if __name__ == '__main__':
    unittest.main()
