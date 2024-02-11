''' Ce module définit des tests pour l'État '''

import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.state import State


class TestState(unittest.TestCase):
    '''
    Cette classe effectue des tests sur l'état
    '''

    def setUp(self):
        '''
        Cette méthode configure toutes les instances nécessaires pour les tests
        '''
        self.storage = FileStorage()
        self.state = State()
        self.state.name = "TestState"
        self.storage.new(self.state)
        self.storage.save()

    def tearDown(self):
        '''
        Cette méthode supprime le fichier json qui a été ouvert pour les tests
        '''
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_state_instance(self):
        ''' Ce test vérifie l'instance de l'état '''
        self.assertIsInstance(self.state, State)

    def test_state_name(self):
        ''' Ce test vérifie le nom de l'état '''
        self.assertEqual(self.state.name, "TestState")


if __name__ == '__main__':
    unittest.main()
