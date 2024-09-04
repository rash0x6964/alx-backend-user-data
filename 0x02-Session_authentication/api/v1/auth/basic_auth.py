#!/usr/bin/env python3
"""Basic authentication module for the API.
"""
import re
import base64
from typing import Tuple, TypeVar

from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic authentication class.
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization header
            for a Basic Authentication.
        """
        if isinstance(authorization_header, str) and \
                authorization_header.startswith("Basic "):
            return authorization_header[len("Basic "):]
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str,
            ) -> str:
        """Decodes a base64-encoded authorization header.
        """
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            res = base64.b64decode(base64_authorization_header)
            return res.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str,
            ) -> Tuple[str, str]:
        """Extracts user credentials from a base64-decoded authorization
            header that uses the Basic authentication flow.
        """
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Retrieves a user based on the user's authentication credentials.
        """
        if not all(isinstance(val, str) for val in [user_email, user_pwd]):
            return None

        users = User.search({"email": user_email})
        if not users:
            return None

        user = users[0]
        return user if user.is_valid_password(user_pwd) else None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the user from a request.
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
