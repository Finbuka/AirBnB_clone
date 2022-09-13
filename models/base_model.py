#!/usr/bin/python3
"""Module for Base class
Contains the Base class for the AirBnB clone console.
"""

import uuid
from datetime import datetime
import models


class BaseModel:
    """Class for base model of object hierarchy."""

    def __init__(self, **kwargs):
        """Initialization of a Base instance.

        Args:
            - *args: list of arguments
            - **kwargs: dict of key-values arguments
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key == "created_at" or key == "updated_at":
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def save(self):
        """Updates the updated_at attribute
        with the current datetime."""
        self.updated_at = datetime.now()
        models.storage.save()

    def __str__(self):
        """Returns a human-readable string representation
        of an instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {str(self.__dict__)}"

    def to_dict(self):
        """Returns a dictionary representation of an instance."""
        return {
            **self.__dict__,
            "__class__": self.__class__.__name__,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
