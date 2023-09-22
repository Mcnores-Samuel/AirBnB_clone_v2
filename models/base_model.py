#!/usr/bin/python3
"""This module define BaseModel class which defines all
common attrbute and methods for subclasses.

Module Description:
The BaseModel module defines the foundational class for all other
classes in the project. It contains attributes and methods that are
common to all classes, ensuring consistent behavior and data structure
across instances. The class is responsible for generating unique IDs,
managing creation and modification timestamps, providing a dictionary
representation of instances, and facilitating serialization and
deserialization through JSON.
"""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, DateTime
from uuid import uuid4

Base = declarative_base()


class BaseModel:
    """BaseModel class  definition"""
    id = Column('id', String(60), nullable=False, primary_key=True)
    created_at = Column('created at', DateTime, nullable=False,
                        default=datetime.utcnow())
    updated_at = Column('updated_at', DateTime, nullable=False,
                        default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiate the BaseModel instance with a unique id,
        the date the instance or object is created,
        and the date at which the instance or object was modified or updated.

        Args:
            args: Won't be used.
            kwargs: Key/value pairs to create another BaseModel object.
        """
        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key == "created_at" or key == "updated_at":
                        value = datetime.strptime(value,
                                                  "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = self.updated_at = datetime.utcnow()

    def __str__(self):
        """Returns the string representation of the BaseModel"""
        self.__dict__.pop('_sa_instance_state', None)
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))

    def save(self):
        """Sets the date at which the BaseModel object has been updated
        and saves it to the storage.
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary representation of the BaseModel object."""
        model_dict = {}
        model_dict["__class__"] = self.__class__.__name__
        for key, value in self.__dict__.items():
            if key == "created_at" or key == "updated_at":
                value = value.isoformat()
            model_dict[key] = value
        model_dict.pop('_sa_instance_state', None)
        return (model_dict)

    def delete(self):
        """Deletes the current instance from storage."""
        models.storage.delete(self)
