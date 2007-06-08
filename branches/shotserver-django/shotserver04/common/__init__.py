import xmlrpclib
import psycopg
from django.db import connection, transaction

MAX_ATTEMPTS = 10


def get_or_fault(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        filters = ' and '.join(
            ['%s=%s' % (key, kwargs[key]) for key in kwargs])
        raise xmlrpclib.Fault(0, '%s not found with %s.' % (
            model.__name__, filters))


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
                    error.message.lower().count("serialize access"))
                if attempt == MAX_ATTEMPTS or not serialize_failed:
                    raise

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper
