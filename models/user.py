#!/usr/bin/python3
"""
User Class from Models Module.
Handles the representation of User objects in the application.
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from hashlib import md5

# Determine the storage type from environment variables
storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class User(BaseModel, Base):
    """
    User class for managing user information in the application.
    Inherits from BaseModel and Base (SQLAlchemy).
    """

    if storage_type == "db":
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column("password", String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)

        # Define relationships with Place and Review
        places = relationship('Place', backref='user', cascade='delete')
        reviews = relationship('Review', backref='user', cascade='delete')
    else:
        # Define attributes for file storage
        email = ''
        password = ''
        first_name = ''
        last_name = ''

    def __init__(self, *args, **kwargs):
        """
        Initialize User Model, inherits from BaseModel.
        :param args: Arguments for BaseModel
        :param kwargs: Keyword arguments for BaseModel
        """
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """
        Getter for password.
        :return: Hashed password
        """
        return self.__dict__.get("password")

    @password.setter
    def password(self, password):
        """
        Setter for password. Hashes the password using MD5 before storing.
        :param password: Plain text password
        """
        self.__dict__["password"] = md5(password.encode('utf-8')).hexdigest()
