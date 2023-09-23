#!/usr/bin/python3
""" Place Module for HBNB project """
import os
import models
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from sqlalchemy import (String, Integer, Column,
                        ForeignKey, Float, Table)
from sqlalchemy.orm import relationship


metadata = Base.metadata


place_amenity = Table("place_amenity", metadata,
                      Column('place_id', String(60), ForeignKey("places.id"),
                             nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey("amenities.id"), nullable=False)
                      )


class Place(BaseModel, Base):
    """A class that represent a rental place and It encompasses
    several attributes including city_id, user_id, name, description,
    number_rooms, number_bathrooms, max_guest,
    price_by_night, latitude, longitude, and amenity_ids
    """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship("Amenity", secondary="place_amenity",
                             viewonly=False)

    if os.environ.get('HBNB_TYPE_STORAGE') != 'db':
        @property
        def review(self):
            """Returns the list of City instances with state_id equals to
            the current State.id => It will be the FileStorage relationship
            between State and City
            """
            reviews_list = []
            reviews_objs = list(models.storage.all(Review).values())
            for review in reviews_objs:
                if review.state_id == self.id:
                    reviews_list.append(review)
            return reviews_list

    @property
    def amenities(self):
        """Returns the list of Amenity instances based on the attribute
        amenity_ids that contains all Amenity.id linked to the Place
        """
        amenities_list = []
        amenities_objs = list(models.storage.all(Amenity).values())
        for amenity in amenities_objs:
            if amenity.id in self.amenity_ids:
                amenities_list.append(amenity)
        return amenities_list

    @amenities.setter
    def amenities(self, amenty_obj):
        """Adds an Amenity.id to the attribute amenity_ids"""
        if type(amenty_obj) == Amenity:
            self.amenity_ids.append(amenty_obj.id)
