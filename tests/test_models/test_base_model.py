import unittest
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test suite for the BaseModel class."""

    def test_init(self):
        """Test initialization of BaseModel instances."""
        model = BaseModel()
        self.assertTrue(hasattr(model, "id"), "No id attribute")
        self.assertTrue(hasattr(model, "created_at"),
                        "No created_at attribute")
        self.assertTrue(hasattr(model, "updated_at"),
                        "No updated_at attribute")

    def test_str(self):
        """Test string representation of BaseModel."""
        model = BaseModel()
        expected = f"[BaseModel] ({model.id}) {model.__dict__}"
        self.assertEqual(str(model), expected)

    def test_save(self):
        """Test the save method updates 'updated_at'."""
        model = BaseModel()
        old_updated_at = model.updated_at
        model.save()
        self.assertNotEqual(model.updated_at, old_updated_at)

    def test_to_dict(self):
        """Test to_dict method returns correct dict."""
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertIsInstance(model_dict['created_at'], str)
        self.assertIsInstance(model_dict['updated_at'], str)


if __name__ == '__main__':
    unittest.main()
