#!/usr/bin/python3
"""
City Class from Models Module
"""

import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey

# Determine the storage type from environment variables
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


class City(BaseModel, Base):
    """
    City class handles all application cities.
    """

    if STORAGE_TYPE == "db":
        # Define table name and columns for database storage
        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

        # Define relationship to Place with cascading delete
        places = relationship('Place', backref='cities', cascade='delete')
    else:
        # Define attributes for file storage
        state_id = ''
        name = ''
        places = []
