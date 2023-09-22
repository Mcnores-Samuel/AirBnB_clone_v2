#!/usr/bin/python3
"""This module provide a DBStorage class for Airbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from os import environ
from models.base_model import Base, BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models.state import State


class DBStorage:
    """Manages and interacts with a MySQL database using the
    SQLAlchemy library. It provides methods for initializing a database
    connection, querying, adding, updating, and deleting data, and managing
    database sessions.

    __engine: A class-level variable that holds the SQLAlchemy database engine.
        This engine is responsible for managing the connection to the MySQL
        database.
    __session: A class-level variable that represents the SQLAlchemy session.
        The session is used to interact with the database, including querying,
        adding, updating, and deleting data.
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initializes an instance of the DBStorage class. It retrieves
        database configuration information from environment variables
        (e.g., database user, password, host, database name, and environment).
        It also creates a SQLAlchemy database engine using the provided
        configuration. If the environment is set to 'test', it drops all
        database tables
        """
        self.db_user = environ.get('HBNB_MYSQL_USER')
        self.password = environ.get('HBNB_MYSQL_PWD')
        self.host = environ.get('HBNB_MYSQL_HOST')
        self.database = environ.get('HBNB_MYSQL_DB')
        self.environment = environ.get('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            self.db_user, self.password, self.host, self.database),
                                      pool_pre_ping=True)
        if self.environment == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Retrieves objects from the database. If a specific class (cls) is
        provided as an argument, it queries objects of that class
        from the database. If no specific class is provided, it queries objects
        from predefined classes (State and City in this case) and returns them
        in a dictionary format with keys in the form of "ClassName.ObjectID"
        and values as the corresponding objects.
        """
        if cls:
            all_objs = self.__session.query(cls).all()
            return {"{}.{}".format(type(obj).__name__,
                               obj.id): obj for obj in all_objs}
        else:
            classes = [State, City]
            data = {}
            for cls in classes:
                query =self.__session.query(cls).all()
                data.update({"{}.{}".format(type(obj).__name__, obj.id): obj for obj in query})
        return data

    def new(self, obj):
        """Adds a new object to the current session. It's typically used
        to stage an object for later saving to the database
        """
        self.__session.add(obj)

    def save(self):
        """Commits changes made in the current session to the database.
        It persists any new objects added and updates any changes made
        to existing objects
        """
        self.__session.commit()

    def delete(self, obj):
        """Deletes an object from the current session. If the object exists
        in the session, it will be removed, and the deletion will be
        reflected when calling save()
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reloads database tables and creates a new session.
        It's used to reset the database session and reinitialize the tables,
        typically after a change to the database schema.
        """
        Base.metadata.create_all(self.__engine)
        main_session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(main_session)
        self.__session = Session()
