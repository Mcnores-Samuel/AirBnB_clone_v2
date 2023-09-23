#!/usr/bin/python3
""" Place Module for HBNB project """
import os
import models
from models.review import Review
from models.base_model import BaseModel, Base
from sqlalchemy import String, Integer, Column, ForeignKey, Float
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """
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
