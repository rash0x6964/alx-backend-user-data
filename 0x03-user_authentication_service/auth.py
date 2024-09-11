#!/usr/bin/env python3
""" Auth module """

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt and return
        the hashed password as bytes.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
