import psycopg
from django.db import connection, transaction

MAX_ATTEMPTS = 3


class ErrorMessage(Exception):

    def __init__(self, message):
        self.message = str(message)


def serializable(func):

    @transaction.commit_manually
    def wrapper(*args, **kwargs):
        if transaction.is_dirty():
            transaction.commit()
        cursor = connection.cursor()
        for attempt in range(1, MAX_ATTEMPTS + 1):
            cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
            try:
                result = func(*args, **kwargs)
                transaction.commit()
                return result
            except Exception, error:
                transaction.rollback()
                serialize_failed = (
                    isinstance(error, psycopg.ProgrammingError) and
                    error.lower().count("can't serialize access"))
                if attempt == MAX_ATTEMPTS or not serialize_failed:
                    raise

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper
