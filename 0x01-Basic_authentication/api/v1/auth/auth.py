#!/usr/bin/env python3
"""Authentication module.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method to check if auth is required.
        """
        if path is None:
            return True

        if not excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif excluded_path == path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Method to get authorization header.
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method to get user from request.
        """
        return None
