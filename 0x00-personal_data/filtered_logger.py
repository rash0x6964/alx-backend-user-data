#!/usr/bin/env python3
""" Filtered logger """

from typing import List, Tuple
import re

import logging

import os
import mysql.connector
from mysql.connector.connection import MySQLConnection


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initializes the formatter with a list of fields to be obfuscated.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Formats the log record by obfuscating specified fields. """
        original_message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, original_message, self.SEPARATOR)


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """ Obfuscates the values of specified fields in a log message. """
    pattern = f'({"|".join([f"{field}=[^{separator}]*" for field in fields])})'
    return re.sub(
        pattern,
        lambda x: x.group().split('=')[0] + f'={redaction}',
        message
    )


PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """ Creates and returns a logger that is configured
        to handle user data logs securely.
    """

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """ Connects to a MySQL database using credentials
        stored in environment variables.
    """
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )
