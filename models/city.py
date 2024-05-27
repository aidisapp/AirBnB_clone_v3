#!/usr/bin/python3
"""
City Class from Models Module.
Handles the representation of City objects in the application.
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey
import models

# Determine the storage type from environment variables
storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class City(BaseModel, Base):
    """
    City class for managing city information in the application.
    Inherits from BaseModel and Base (SQLAlchemy).
    """

    if storage_type == "db":
        # Define the table name for database storage
        __tablename__ = 'cities'

        # Define the 'name' column for the cities table
        name = Column(String(128), nullable=False)

        # Define the 'state_id' column as a foreign key
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

        # Define the one-to-many relationship with Place
        places = relationship('Place', backref='cities', cascade='delete')
    else:
        # Define attributes for file storage
        state_id = ''
        name = ''

    if storage_type != 'db':
        @property
        def places(self):
            """
            Getter method for retrieving places related to the city.
            :return: List of Place instances that belong to this city.
            """
            all_places = models.storage.all("Place")
            result = []

            for obj in all_places.values():
                if str(obj.city_id) == str(self.id):
                    result.append(obj)

            return result
