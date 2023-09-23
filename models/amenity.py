#!/usr/bin/python3
"""Amenity class module

Class Description:
The Amenity class represents various amenities that might be
associated with accommodations or other facilities. It has a single
attribute named name, which stores the name of the amenity.
Instances of this class provide a standardized way of
categorizing and managing amenities.
"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Amenity class that inherits from BaseModel and has
    attrbute name for the amenity name.
    """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary="place_amenity",
                                   viewonly=False)
