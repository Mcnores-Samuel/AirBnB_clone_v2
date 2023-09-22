#!/usr/bin/python3
"""A state class module

Class Description:
The State class represents a geographical state and is part of the data model.
It has a name attribute, which stores the name of the state. Instances of this
class serve as a means of organizing and categorizing locations within a larger
geographical context.
"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
import os
import models


class State(BaseModel, Base):
    """A state class with a name attributes to represent
    geographical state.
    """
    __tablename__ = "states"
    name = Column('name', String(128), nullable=False)
    cities = relationship('City', backref='state', cascade='all,\
                          delete-orphan')

    if os.environ.get('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """Returns the list of City instances with state_id equals to
            the current State.id => It will be the FileStorage relationship
            between State and City
            """
            cities_list = []
            cities_objs = list(models.storage.all(City).values())
            for city in cities_objs:
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
