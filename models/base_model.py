#!/usr/bin/python3
"""
BaseModel Class of Models Module.
Handles the core attributes and methods for all models.
"""

import os
import json
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

# Determine the storage type from environment variables
storage_type = os.environ.get('HBNB_TYPE_STORAGE')

"""
Create an instance of Base if storage type is a database.
If not using database storage, define a placeholder Base class.
"""
if storage_type == 'db':
    Base = declarative_base()
else:
    class Base:
        pass


class BaseModel:
    """
    BaseModel class that defines all common attributes
    and methods for other classes.
    """
    if storage_type == 'db':
        # Define columns for database storage
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(
            DateTime, nullable=False, default=datetime.utcnow)
        updated_at = Column(
            DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
        Instantiation of a new BaseModel instance.
        :param args: Unused.
        :param kwargs: Key-value pairs of attributes.
        """
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    setattr(self, key, value)

    def __is_serializable(self, obj_v):
        """
        Checks if an object is serializable to JSON.
        :param obj_v: The object to check.
        :return: True if serializable, False otherwise.
        """
        try:
            obj_to_str = json.dumps(obj_v)
            return isinstance(obj_to_str, str)
        except (TypeError, ValueError):
            return False

    def bm_update(self, name, value):
        """
        Updates the attribute of the BaseModel instance.
        :param name: The name of the attribute to update.
        :param value: The value to set the attribute to.
        """
        setattr(self, name, value)
        if storage_type != 'db':
            self.save()

    def save(self):
        """
        Updates the `updated_at` attribute to the
        current time and saves the instance.
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_json(self):
        """
        Returns a JSON representation of the instance.
        :return: Dictionary representation of the instance.
        """
        bm_dict = {}
        for key, value in self.__dict__.items():
            if self.__is_serializable(value):
                bm_dict[key] = value
            else:
                bm_dict[key] = str(value)
        bm_dict['__class__'] = type(self).__name__
        bm_dict.pop('_sa_instance_state', None)
        if storage_type == "db" and 'password' in bm_dict:
            bm_dict.pop('password')
        return bm_dict

    def __str__(self):
        """
        Returns a string representation of the instance.
        :return: String representation in the format [ClassName]
        (id) {attributes}.
        """
        class_name = type(self).__name__
        return '[{}] ({}) {}'.format(class_name, self.id, self.__dict__)

    def delete(self):
        """
        Deletes the current instance from storage.
        """
        models.storage.delete(self)
