#!/usr/bin/env python3
"""
Module for data filtering with obfuscation capabilities.
This module contains a function to obfuscate specified fields in a log message.
"""

import re
from typing import List

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message.
    
    Args:
        fields (List[str]): Fields to be obfuscated.
        redaction (str): String to replace the obfuscated values.
        message (str): The original log message.
        separator (str): Character separating fields in the log line.
        
    Returns:
        str: The modified log message with fields obfuscated.
    """
    return re.sub(f"({'|'.join(fields)})=[^{separator}]*", lambda m: f"{m.group(1)}={redaction}", message)
