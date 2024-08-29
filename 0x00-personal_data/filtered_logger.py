#!/usr/bin/env python3
"""  """

from typing import List
import re


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
