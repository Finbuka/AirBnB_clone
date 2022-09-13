#!/usr/bin/python3
"""Module for FileStorage class."""

import json
import os

from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Class for serializtion and deserialization of base classes."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns __objects dictionary."""
        return FileStorage.__objects

    def new(self, obj):
        """Sets new obj in __objects dictionary."""
        FileStorage.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """Serialzes __objects to JSON file."""
        with open(FileStorage.__file_path, "w") as f:

            obj_dict = FileStorage.__objects
            json.dump(
                {key: value.to_dict() for key, value in obj_dict.items()},
                f,
                indent=4,
            )

    def reload(self):
        """Deserializes JSON file into __objects."""
        if os.path.exists(FileStorage.__file_path):
            with open(self.__file_path, "r") as f:
                tmp = json.load(f)
            for key, value in tmp.items():
                FileStorage.__objects[key] = eval(value["__class__"])(**value)
