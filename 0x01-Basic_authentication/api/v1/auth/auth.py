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
        return None;
    
    
    def authorization_header(self, request=None) -> str:
        return None;
    
    
    def current_user(self, request=None) -> TypeVar('User'):
        return None;
     