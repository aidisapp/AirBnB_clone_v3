#!/usr/bin/python3
"""
State Class from Models Module.
Handles the representation of State objects in the application.
"""
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models


class State(BaseModel, Base):
    """
    State class for managing state information in the application.
    Inherits from BaseModel and Base (SQLAlchemy).
    """
    __tablename__ = "states"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        name = ""

        @property
        def cities(self):
            """
            Getter method for cities.
            :return: List of City objects associated with the current State.
            """
            list_cities = []
            for city in models.storage.all("City").values():
                if city.state_id == self.id:
                    list_cities.append(city)
            return list_cities
