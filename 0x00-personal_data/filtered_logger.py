#!/usr/bin/env python3
""" Filtered logger """

from typing import List
import re

import logging


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
