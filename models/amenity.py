#!/usr/bin/python3
"""
Amenity Class from Models Module.
Handles the representation of Amenity objects in the application.
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String

storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class Amenity(BaseModel, Base):
    """
    Amenity class for managing application amenities.
    Inherits from BaseModel and Base (SQLAlchemy).
    """
    if storage_type == "db":
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)

        # Define the many-to-many relationship with Place
        place_amenities = relationship("Place", secondary="place_amenity")
    else:
        # Define 'name' attribute for file storage
        name = ''
