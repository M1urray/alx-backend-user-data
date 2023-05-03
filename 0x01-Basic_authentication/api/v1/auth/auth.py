#!/usr/bin/env python3
"""
Class to manage the API authentication
"""
from flask import request
from typing import TypeVar, List


class Auth:
    '''
    manage the API authentication
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks whether a path requires authentication.
        """
        if not path or not excluded_paths:
            return True
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path):
                return False
        return True


    def authorization_header(self, request=None) -> str:
        ''' def authorization_header '''
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']


    def current_user(self, request=None) -> TypeVar('User'):
        ''' def current_user 
        '''
        return None
     