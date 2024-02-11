#!/usr/bin/python3
''' This modules defines tests for the file storage '''
import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):
    '''
    This class conducts test on the storage
    facility of this project
    '''

    def setUp(self):
        '''
        This method sets up all instances needed for testing
        '''
        self.storage = FileStorage()
        self.base_model = BaseModel()
        self.base_model_dict = self.base_model.to_dict()
        self.storage.new(self.base_model)
        self.storage.save()

    def tearDown(self):
        '''
        The method tears down the json file that was open for testing
        '''
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_json_file_exist(self):
        ''' This tests for the existence of the json file
        upon creating an instance of the class FileStorage'''
        self.assertTrue(os.path.exists(FileStorage._FileStorage__file_path))

    def test_all(self):
        ''' Test for "all" function of the storage class to ensure
        that the dictionary representation of the class instance is stored
        in __objects'''
        objects = self.storage.all()
        key = self.base_model.__class__.__name__ + "." + self.base_model.id
        self.assertTrue(isinstance(objects, dict))
        self.assertTrue(isinstance(objects[key], BaseModel))
        self.assertIn(key, objects)

    def test_new(self):
        ''' Test for the new method '''
        new_model = BaseModel()
        self.storage.new(new_model)
        objects = self.storage.all()
        key = new_model.__class__.__name__ + "." + new_model.id
        self.assertIn(key, objects)
        self.assertTrue(isinstance(objects[key], BaseModel))

    def test_save_reload(self):
        '''Test for the save an dreload methods'''
        self.storage.save()
        objects_before_reload = self.storage.all()
        self.storage.reload()
        objects_after_reload = self.storage.all()
        self.assertEqual(objects_before_reload, objects_after_reload)

    def test_json_file_content(self):
        '''Tests for the content of the json file'''
        with open(FileStorage._FileStorage__file_path, 'r') as f:
            file_content = f.read()
            file_data = json.loads(file_content)
            self.assertIn(
                    self.base_model.__class__.__name__ +
                    "." + self.base_model.id, file_data
                    )


if __name__ == '__main__':
    unittest.main()
