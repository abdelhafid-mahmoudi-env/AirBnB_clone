''' Ce module définit les tests pour la console '''

import unittest
from console import HBNBCommand
from unittest.mock import patch
import os
from io import StringIO
from models import storage


class TestConsole(unittest.TestCase):
    '''
    Cette classe effectue des tests sur la console
    '''

    def setUp(self):
        ''' Mise en place du test '''
        self.console = HBNBCommand()

    def tearDown(self):
        ''' Nettoyage après le test '''
        self.console = None

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     'This test only work in Filestorage')
    def test_create(self):
        ''' Test create '''
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create State name='California'")
            state_id = f.getvalue().strip()
            self.assertTrue(len(state_id) == 36)
            self.assertTrue(os.path.exists('file.json'))
            storage.delete(State(state_id))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     'This test only work in Filestorage')
    def test_show(self):
        ''' Test show '''
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create State name='California'")
            state_id = f.getvalue().strip()
            self.console.onecmd("show State " + state_id)
            self.assertIn(state_id, f.getvalue().strip())
            self.assertIn("'name': 'California'", f.getvalue().strip())
            storage.delete(State(state_id))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     'This test only work in Filestorage')
    def test_destroy(self):
        ''' Test destroy '''
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create State name='California'")
            state_id = f.getvalue().strip()
            self.console.onecmd("destroy State " + state_id)
            self.assertNotIn(state_id, storage.all().keys())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     'This test only work in Filestorage')
    def test_all(self):
        ''' Test all '''
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create State name='California'")
            self.console.onecmd("create State name='Arizona'")
            self.console.onecmd("create State name='Nevada'")
            self.console.onecmd("all State")
            self.assertIn("'California'", f.getvalue().strip())
            self.assertIn("'Arizona'", f.getvalue().strip())
            self.assertIn("'Nevada'", f.getvalue().strip())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     'This test only work in Filestorage')
    def test_update(self):
        ''' Test update '''
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create State name='California'")
            state_id = f.getvalue().strip()
            self.console.onecmd("update State " + state_id + " name 'New_York'")
            self.console.onecmd("show State " + state_id)
            self.assertIn("'name': 'New_York'", f.getvalue().strip())
            storage.delete(State(state_id))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     'This test only work in Filestorage')
    def test_count(self):
        ''' Test count '''
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create State name='California'")
            self.console.onecmd("create State name='Arizona'")
            self.console.onecmd("create City name='LA' state_id='" +
                                list(storage.all("State").values())[0].id + "'")
            self.console.onecmd("count State")
            self.assertEqual("2", f.getvalue().strip())
            self.console.onecmd("count City")
            self.assertEqual("1", f.getvalue().strip())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     'This test only work in Filestorage')
    def test_dump(self):
        ''' Test dump '''
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create State name='California'")
            self.console.onecmd("create State name='Arizona'")
            self.console.onecmd("create City name='LA' state_id='" +
                                list(storage.all("State").values())[0].id + "'")
            self.console.onecmd("create City name='SF' state_id='" +
                                list(storage.all("State").values())[1].id + "'")
            self.console.onecmd("dump")
            with open("file.json", "r") as file:
                self.assertEqual(len(file.readlines()), 6)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     'This test only work in Filestorage')
    def test_restore(self):
        ''' Test restore '''
        self.console.onecmd("create State name='California'")
        self.console.onecmd("create State name='Arizona'")
        self.console.onecmd("create City name='LA' state_id='" +
                            list(storage.all("State").values())[0].id + "'")
        self.console.onecmd("create City name='SF' state_id='" +
                            list(storage.all("State").values())[1].id + "'")
        self.console.onecmd("destroy State " + list(storage.all("State").values())[0].id)
        self.console.onecmd("destroy State " + list(storage.all("State").values())[1].id)
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all")
            self.assertEqual("", f.getvalue().strip())
            self.console.onecmd("restore")
            self.console.onecmd("all")
            output = f.getvalue().strip().split("\n")
            self.assertEqual(len(output), 4)
            self.assertIn("California", output[0])
            self.assertIn("Arizona", output[1])
            self.assertIn("LA", output[2])
            self.assertIn("SF", output[3])


if __name__ == '__main__':
    unittest.main()
