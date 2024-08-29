#!/usr/bin/env python3
""" Encrypt password """

import bcrypt


def hash_password(password: str) -> bytes:
    """ Hashes a password using bcrypt with a generated salt """
    password_bytes = password.encode('utf-8')
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Checks if the provided password matches the hashed password """
    password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)
