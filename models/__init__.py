#!/usr/bin/python3
from .engine.file_storage import FileStorage

# Create an instance of FileStorage
storage = FileStorage()
# Reload objects from file to __objects dictionary, if file exists
storage.reload()
