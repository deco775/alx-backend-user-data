#!/usr/bin/env python3
"""
Module for securely hashing passwords.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password with a random salt using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    salt = bcrypt.gensalt()  # Generate a salt
    hashed = bcrypt.hashpw(password.encode(), salt)  # Hash the password with the salt
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that a password matches a given hashed password.

    Args:
        hashed_password (bytes): The hashed password to check against.
        password (str): The plain text password to verify.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
