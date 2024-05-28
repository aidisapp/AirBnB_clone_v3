#!/usr/bin/python3
"""
Amenity Class from Models Module.
Handles the representation of Amenity objects in the application.
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String

# Determine the storage type from environment variables
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


class Amenity(BaseModel, Base):
    """
    Amenity class for managing amenity information in the application.
    Inherits from BaseModel and Base (SQLAlchemy).
    """
    if STORAGE_TYPE == "db":
        # Define the table name for database storage
        __tablename__ = 'amenities'

        # Define the 'name' column for storing the amenity name
        name = Column(String(128), nullable=False)

        # Define the relationship with PlaceAmenity
        place_amenities = relationship(
            'PlaceAmenity', backref='amenities', cascade='delete')
    else:
        # Define attributes for file storage
        name = ''
