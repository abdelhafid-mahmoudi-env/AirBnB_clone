#!/usr/bin/python3
"""
Initializes the models package
"""
from models.engine.file_storage import FileStorage

# Initialize the class registry dictionary
class_registry = {}

def register_class(cls):
    """
    Registers a class in the class registry.
    """
    class_registry[cls.__name__] = cls

def get_class_by_name(name):
    """
    Retrieves a class from the class registry by name.
    """
    return class_registry.get(name)

# Create an instance of FileStorage
storage = FileStorage()
# Reload objects from file to __objects dictionary, if file exists
storage.reload()
