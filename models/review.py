#!/usr/bin/python3
"""
Review Class from Models Module.
Handles the representation of Review objects in the application.
"""
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Review(BaseModel, Base):
    """
    Review class for managing review information in the application.
    Inherits from BaseModel and Base (SQLAlchemy).
    """
    __tablename__ = "reviews"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    else:
        # Define attributes for file storage
        place_id = ""
        user_id = ""
        text = ""
