#!/usr/bin/python3
"""
Review Class from Models Module.
Handles the representation of Review objects in the application.
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey

# Determine the storage type from environment variables
storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class Review(BaseModel, Base):
    """
    Review class for managing review information in the application.
    Inherits from BaseModel and Base (SQLAlchemy).
    """

    if storage_type == "db":
        __tablename__ = 'reviews'
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        # Define attributes for file storage
        place_id = ''
        user_id = ''
        text = ''
