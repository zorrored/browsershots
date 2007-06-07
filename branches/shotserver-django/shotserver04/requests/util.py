import psycopg
from datetime import datetime, timedelta
from django.db import connection, transaction
from shotserver04.xmlrpc import ErrorMessage
from shotserver04.requests.models import Request

MAX_ATTEMPTS = 3


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


@serializable
def find_and_lock_request(factory, features):
    # Find matching request
    five_minutes_ago = datetime.now() - timedelta(0, 300)
    matches = Request.objects.select_related()
    matches = matches.filter(features)
    matches = matches.filter(uploaded__isnull=True)
    matches = matches.filter(
        Q(locked__isnull=True) | Q(locked__lt=five_minutes_ago))
    matches = matches.order_by(
        '-requests_request__request_group.submitted')
    matches = matches[:1]
    if len(matches) == 0:
        raise ErrorMessage('No matching request.')
    request = matches[0]
    # Lock request
    request.factory = factory
    request.locked = datetime.now()
    request.save()
    return request
