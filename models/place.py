#!/usr/bin/python3
"""
Place Class from Models Module.
Handles the representation of Place objects in the application.
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
import models

# Determine the storage type from environment variables
storage_type = os.environ.get('HBNB_TYPE_STORAGE')

# Create the association table for the many-to-many relationship
if storage_type == "db":
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id')),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id',
                                            ondelete="CASCADE")))


class Place(BaseModel, Base):
    """
    Place class for managing place information in the application.
    Inherits from BaseModel and Base (SQLAlchemy).
    """

    if storage_type == "db":
        # Define the table name for database storage
        __tablename__ = 'places'

        # Define the columns for the places table
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

        # Define the many-to-many relationship with Amenity
        amenities = relationship('Amenity',
                                 secondary="place_amenity", viewonly=False)

        # Define the one-to-many relationship with Review
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

    if storage_tpe != "db":
        @property
        def amenities(self):
            """
            Getter for amenities.
            :return: List of Amenity instances associated with this Place.
            """
            amenity_objs = []
            for a_id in self.amenity_ids:
                amenity_objs.append(models.storage.get("Amenity", str(a_id)))
            return amenity_objs

        @amenities.setter
        def amenities(self, amenity):
            """
            Setter for amenities. Adds the Amenity id to the amenity_ids list.
            :param amenity: The Amenity instance to add.
            """
            self.amenity_ids.append(amenity.id)

        @property
        def reviews(self):
            """
            Getter for reviews.
            :return: List of Review instances associated with this Place.
            """
            all_reviews = models.storage.all("Review")
            place_reviews = [review for review in all_reviews.values()
                             if review.place_id == self.id]
            return place_reviews
