#!/usr/bin/python3
"""
State Class from Models Module.
Handles the representation of State objects in the application.
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
import models

# Determine the storage type from environment variables
storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class State(BaseModel, Base):
    """
    State class for managing state information in the application.
    Inherits from BaseModel and Base (SQLAlchemy).
    """

    if storage_type == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state', cascade='delete')
    else:
        # Define attributes for file storage
        name = ''

    if storage_type != 'db':
        @property
        def cities(self):
            """
            Getter method for cities.
            :return: List of City objects associated with the current State.
            """
            city_list = []
            for city in models.storage.all("City").values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
