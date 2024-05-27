#!/usr/bin/python3
"""
Database engine module for managing long-term storage of class instances.
"""

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models import base_model, amenity, city, place, review, state, user


class DBStorage:
    """Handles long-term storage of all class instances using SQLAlchemy."""

    # Mapping of class names to class objects
    CNC = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }

    # Private attributes for SQLAlchemy engine and session
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the SQLAlchemy engine."""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.environ.get('HBNB_MYSQL_USER'),
                os.environ.get('HBNB_MYSQL_PWD'),
                os.environ.get('HBNB_MYSQL_HOST'),
                os.environ.get('HBNB_MYSQL_DB')))
        # Drop all tables if the environment is set to 'test'
        if os.environ.get("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Returns a dictionary of all objects of a specified class.
        If no class is specified, returns all objects of all classes.
        :param cls: (Optional) Class name as a string
        :return: Dictionary of objects with keys formatted as
        <class name>.<object id>
        """
        obj_dict = {}
        if cls:
            # Query all instances of the specified class
            obj_class = self.__session.query(self.CNC.get(cls)).all()
            for item in obj_class:
                key = f"{item.__class__.__name__}.{item.id}"
                obj_dict[key] = item
            return obj_dict

        # Query all instances of all classes
        for class_name in self.CNC:
            if class_name == 'BaseModel':
                continue
            obj_class = self.__session.query(self.CNC.get(class_name)).all()
            for item in obj_class:
                key = f"{item.__class__.__name__}.{item.id}"
                obj_dict[key] = item
        return obj_dict

    def new(self, obj):
        """
        Adds an object to the current database session.
        :param obj: The object to be added to the session
        """
        self.__session.add(obj)

    def get(self, cls, id):
        """
        Fetches a specific object by class name and ID.
        :param cls: Class name as a string
        :param id: Object ID as a string
        :return: The found object or None if not found
        """
        all_class = self.all(cls)
        for obj in all_class.values():
            if id == str(obj.id):
                return obj
        return None

    def count(self, cls=None):
        """
        Counts the number of instances of a specified class.
        If no class is specified, counts instances of all classes.
        :param cls: (Optional) Class name as a string
        :return: Number of instances of the specified class
        """
        return len(self.all(cls))

    def save(self):
        """Commits all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the current database session if it is not None.
        :param obj: The object to be deleted
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database and initializes the session."""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))

    def close(self):
        """Closes the current database session by calling remove()."""
        self.__session.remove()
