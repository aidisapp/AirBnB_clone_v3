#!/usr/bin/python3
"""
Place Class from Models Module
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table

# Determine the storage type from environment variables
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')

# Define the Place Amenity table for many-to-many relationship
if STORAGE_TYPE == "db":
    class PlaceAmenity(Base):
        """
        PlaceAmenity Class to handle the many-to-many relationship
        between Place and Amenity
        """
        __tablename__ = 'place_amenity'
        metadata = Base.metadata
        place_id = Column(String(60),
                          ForeignKey('places.id'),
                          nullable=False,
                          primary_key=True)
        amenity_id = Column(String(60),
                            ForeignKey('amenities.id'),
                            nullable=False,
                            primary_key=True)


class Place(BaseModel, Base):
    """Place class handles all application places"""

    if STORAGE_TYPE == "db":
        # Define table name and columns for database storage
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

        # Define relationships with other tables
        amenities = relationship('Amenity', secondary='place_amenity',
                                 viewonly=False)
        reviews = relationship('Review', backref='place', cascade='delete')
    else:
        # Define attributes for file storage
        city_id = ''
        user_id = ''
        name = ''
        description = ''
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []
        review_ids = []

        @property
        def amenities(self):
            """
                Getter for the amenities list, retrieves the
                amenities associated with the place
            """
            if self.amenity_ids:
                return self.amenity_ids
            return None

        @amenities.setter
        def amenities(self, amenity_obj):
            """
                Setter for the amenities list, adds a new
                amenity ID if it's not already in the list
            """
            if amenity_obj and amenity_obj.id not in self.amenity_ids:
                self.amenity_ids.append(amenity_obj.id)

        @property
        def reviews(self):
            """
                Getter for the reviews list, retrieves
                the reviews associated with the place
            """
            if self.review_ids:
                return self.review_ids
            return None

        @reviews.setter
        def reviews(self, review_obj):
            """
                Setter for the reviews list, adds a new review
                ID if it's not already in the list
            """
            if review_obj and review_obj.id not in self.review_ids:
                self.review_ids.append(review_obj.id)
