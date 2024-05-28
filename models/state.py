#!/usr/bin/python3
"""
State Class from Models Module
"""
import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String

# Fetch the storage type from environment variables
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


class State(BaseModel, Base):
    """State class handles all application states"""

    if STORAGE_TYPE == "db":
        # Define table name and columns for database storage
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)

        # Relationship with City class for database storage
        cities = relationship('City', backref='state', cascade='delete')
    else:
        # Define attribute for file storage
        name = ''

        @property
        def cities(self):
            """
            Getter method to retrieve list of City objects
            linked to the current State.
            """
            city_list = []
            for city in models.storage.all("City").values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
