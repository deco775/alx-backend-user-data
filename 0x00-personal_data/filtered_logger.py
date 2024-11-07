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

#!/usr/bin/env python3
"""
Module for a custom RedactingFormatter in logging to obfuscate sensitive fields.
"""

import logging
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


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class for obfuscating sensitive fields in log messages.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes the RedactingFormatter.

        Args:
            fields (List[str]): A list of field names to be obfuscated.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a log record by obfuscating sensitive fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted and obfuscated log record.
        """
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_message, self.SEPARATOR)

Use user_data.csv for this task

Implement a get_logger function that takes no arguments and returns a logging.Logger object.

The logger should be named "user_data" and only log up to logging.INFO level. It should not propagate messages to other loggers. It should have a StreamHandler with RedactingFormatter as formatter.

Create a tuple PII_FIELDS constant at the root of the module containing the fields from user_data.csv that are considered PII. PII_FIELDS can contain only 5 fields - choose the right list of fields that can are considered as “important” PIIs or information that you must hide in your logs. Use it to parameterize the formatter.

#!/usr/bin/env python3
"""
Module for retrieving and logging user data from a database with sensitive fields redacted.
"""

import os
import mysql.connector
import logging
from typing import List
from mysql.connector import connection
from datetime import datetime

# Define the fields from user_data.csv that are considered PII.
PII_FIELDS: tuple = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class for obfuscating sensitive fields in log messages.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes the RedactingFormatter.

        Args:
            fields (List[str]): A list of field names to be obfuscated.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a log record by obfuscating sensitive fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted and obfuscated log record.
        """
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_message, self.SEPARATOR)


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


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger named "user_data" with obfuscation for sensitive fields.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """
    Connects to a secure MySQL database using credentials from environment variables.

    Environment Variables:
        PERSONAL_DATA_DB_USERNAME: Database username (default: "root").
        PERSONAL_DATA_DB_PASSWORD: Database password (default: "").
        PERSONAL_DATA_DB_HOST: Database host (default: "localhost").
        PERSONAL_DATA_DB_NAME: Database name (required).

    Returns:
        mysql.connector.connection.MySQLConnection: A connection to the MySQL database.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    # Create a connection to the database
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )


def main():
    """
    Main function to retrieve and log user data with sensitive fields redacted.
    """
    db = get_db()
    logger = get_logger()

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")

    for row in cursor:
        # Format each row as a log message with sensitive fields redacted
        message = "; ".join(f"{k}={v}" for k, v in row.items())
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
