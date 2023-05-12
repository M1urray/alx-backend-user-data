#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from user import Base, User
from typing import TypeVar
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:

    def __init__(self):
        ''' def init '''
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar('User'):
        """_summary_

        Args:
            self, email (str): user email, hashed_password (str): user password

        Returns:
            user: return user model
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kargs) -> TypeVar('User'):
        """_summary_

        Args:
            self (_type_): _description_

        Raises:
            InvalidRequestError: type error
            NoResultFound: no result found

        Returns:
            user: return user model
        """
        try:
            user = self._session.query(User).filter_by(**kargs).first()
        except TypeError:
            raise InvalidRequestError
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user
        """
        user = self.find_user_by(id=user_id)
        for x, y in kwargs.items():
            if hasattr(user, x):
                setattr(user, x, y)
            else:
                raise ValueError
        self._session.commit()
