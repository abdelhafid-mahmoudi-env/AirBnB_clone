''' Ce module définit des tests pour l'aménité '''

import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    '''
    Cette classe effectue des tests sur l'aménité
    '''

    def setUp(self):
        '''
        Cette méthode configure toutes les instances nécessaires pour les tests
        '''
        self.storage = FileStorage()
        self.amenity = Amenity()
        self.amenity.name = "TestAmenity"
        self.storage.new(self.amenity)
        self.storage.save()

    def tearDown(self):
        '''
        Cette méthode supprime le fichier json qui a été ouvert pour les tests
        '''
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_amenity_instance(self):
        ''' Ce test vérifie l'instance de l'aménité '''
        self.assertIsInstance(self.amenity, Amenity)

    def test_amenity_name(self):
        ''' Ce test vérifie le nom de l'aménité '''
        self.assertEqual(self.amenity.name, "TestAmenity")


if __name__ == '__main__':
    unittest.main()
