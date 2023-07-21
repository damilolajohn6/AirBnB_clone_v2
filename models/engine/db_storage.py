#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""


from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import (create_engine)
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from os import getenv

classes = {
    "City": City,
    "State": State,
    "User": User,
    "Place": Place,
    "Review": Review,
    "Amenity": Amenity
}


class DBStorage():
    """This class manages storage of hbnb models to MySQL Server db
        Attributes:
            __engine (sqlalchemy.Engine) : the working SQLAlchemy engine
            __session (sqlalchemy.Session) : theworking SQLAlchemy session
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialises a new DBStorage instance"""

        dialect = "mysql"
        driver = "mysqldb"
        port = 3306
        user = getenv('HBNB_MYSQL_USER')
        passwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db_name = getenv('HBNB_MYSQL_DB')

        db_uri = \
            f'{dialect}+{driver}://{user}:{passwd}@{host}:{port}/{db_name}'
        self.__engine = create_engine(db_uri, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries all objects on the current database session
        (self.__session)
        depending of the class name (argument cls)
            Returns a dictionary: key = <class-name>.<object-id>,
            value = object
        """
        dictionary = {}
        if cls:
            # Return all objects in given Class
            if isinstance(cls, str):
                cls = classes[cls]

            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + "." + obj.id
                dictionary[key] = obj
        else:
            # query all types of objects (User, State, City, Amenity, Place and
            # Review
            for _cls in classes.values():
                objs = objs = self.__session.query(_cls).all()

                for obj in objs:
                    key = obj.__class__.__name__ + "." + obj.id
                dictionary[key] = obj

        return dictionary

    def new(self, obj):
        """
        Adds an object to the current database session (self.__session)
        """

        self.__session.add(obj)

    def save(self):
        """
        Commits all changes of the current database session (self.__session)
        """

        self.__session.commit()

    def reload(self):
        """
        Creates all tables in the database (feature of SQLAlchemy)
            Creates the current database session (self.__session)
            from the engine (self.__engine)
        """
        # all classes who inherit from Base must be imported before calling
        # this fn
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def delete(self, obj=None):
        """
        delete an object(if it exists) from the current database session
        """
        if obj:
            self.__session.delete(obj)

    def close(self):
        """ Closes the working SQLAlchemy session """
        self.__session.close()
