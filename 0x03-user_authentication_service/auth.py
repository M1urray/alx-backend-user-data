#!/usr/bin/env python3
''' Hashed Module '''

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> str:
    """Hash user password using bcrypt
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    ''' def generate uid '''
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register new user
        """
        if email and password:
            try:
                self._db.find_user_by(email=email)
            except NoResultFound:
                user = self._db.add_user(email, _hash_password(password))
                return user
            else:
                raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """_summary_

        Args:
            email (str): _description_
            password (str): _description_

        Returns:
            bool: _description_
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """_summary_

        Args:
            email (str): user email

        Returns:
            str: session_id
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> str:
        """_summary_

        Args:
            session_id (str): _description_

        Returns:
            str: _description_
        """
        if not session_id:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return

    def destroy_session(self, user_id: int) -> None:
        """_summary_

        Args:
            user_id (int): _description_
        """
        if user_id:
            self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """_summary_

        Args:
            email (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if email:
            try:
                user = self._db.find_user_by(email=email)
            except NoResultFound:
                raise ValueError
            else:
                take = _generate_uuid()
                self._db.update_user(user.id, reset_token=take)
                return take

    def update_password(self, reset_token: str, password: str) -> None:
        """_summary_

        Args:
            reset_token (str): _description_
            password (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            n_pass = _hash_password(password)
            self._db.update_user(user.id, hashed_password=n_pass,
                                 reset_token=None)
            return None
        except Exception:
            raise ValueError
