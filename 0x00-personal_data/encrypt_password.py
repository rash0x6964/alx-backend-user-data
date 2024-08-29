#!/usr/bin/env python3
""" Encrypt password """

import bcrypt


def hash_password(password: str) -> bytes:
    """ Hashes a password using bcrypt with a generated salt """
    password_bytes = password.encode('utf-8')
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())
