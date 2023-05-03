#!/usr/bin/env python3
"""
Class to manage the API authentication
"""
import re
from flask import request
from typing import TypeVar, List


class Auth:
    '''
    manage the API authentication
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks whether a path requires authentication.
        """
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
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
     