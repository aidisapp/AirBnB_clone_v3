#!/usr/bin/python3
"""
User Class from Models Module
"""
import hashlib
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String

# Fetch the storage type from environment variables
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


class User(BaseModel, Base):
    """
    User class handles all application users
    """

    if STORAGE_TYPE == "db":
        # Define table name and columns for database storage
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)

        # Relationships with other classes for database storage
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
        Instantiate a User object.
        If 'password' is provided in kwargs, encrypt it and set it.
        """
        if kwargs:
            # If 'password' is provided, encrypt it and set it
            pwd = kwargs.pop('password', None)
            if pwd:
                User.__set_password(self, pwd)
        super().__init__(*args, **kwargs)

    def __set_password(self, pwd):
        """
        Custom setter method to encrypt password using MD5.
        """
        # Encrypt password using MD5 algorithm
        secure = hashlib.md5()
        secure.update(pwd.encode("utf-8"))
        secure_password = secure.hexdigest()

        # Set the encrypted password attribute
        setattr(self, "password", secure_password)
