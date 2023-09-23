#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        if cls:
            if type(cls) == str:
                cls = classes[cls]
            data = self.__objects
            all_cls_objs = {}
            for key in data.keys():
                instance = key.split(".")[0]
                if cls.__name__ == instance:
                    all_cls_objs[key] = data[key]
            return all_cls_objs
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id

        args:
            obj: A dictionary to be set as a value to <obj class name>.id
            as key/pair values of __objects dictionary.
        Returns: nothing
        """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it’s inside - if obj is equal to None,
        does nothing:

        args:
            obj: an object to delete from the file_storage.
        """
        if obj:
            all_objs = self.__objects
            for current_obj in all_objs.keys():
                cur_obj_id = current_obj.split(".")[1]
                if obj.id == cur_obj_id:
                    del all_objs[current_obj]
                    self.save()
                    break
