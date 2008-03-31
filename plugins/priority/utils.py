from datetime import datetime


def expiration_date(activated, months):
    """
    >>> expiration_date(datetime(2008, 1, 1), 1)
    datetime.datetime(2008, 2, 1, 0, 0)
    >>> expiration_date(datetime(2008, 1, 2), 1)
    datetime.datetime(2008, 2, 2, 0, 0)
    >>> expiration_date(datetime(2008, 1, 29), 1)
    datetime.datetime(2008, 2, 29, 0, 0)
    >>> expiration_date(datetime(2008, 1, 30), 1)
    datetime.datetime(2008, 2, 29, 0, 0)
    >>> expiration_date(datetime(2008, 1, 31), 1)
    datetime.datetime(2008, 2, 29, 0, 0)
    >>> expiration_date(datetime(2008, 12, 31), 1)
    datetime.datetime(2009, 1, 31, 0, 0)
    >>> expiration_date(datetime(2008, 1, 1), 12)
    datetime.datetime(2009, 1, 1, 0, 0)
    >>> expiration_date(datetime(2008, 12, 31), 12)
    datetime.datetime(2009, 12, 31, 0, 0)
    >>> expiration_date(datetime(2008, 2, 29), 12)
    datetime.datetime(2009, 2, 28, 0, 0)
    """
    year, month, day, hour, minute, sec = activated.timetuple()[:6]
    month += months
    if month > 12:
        year += 1
        month -= 12
    while True:
        try:
            return datetime(year, month, day, hour, minute, sec)
        except ValueError:
            if day <= 28:
                raise
            day -= 1 # February 31st doesn't exist, reduce and try again.


if __name__ == '__main__':
    import doctest
    doctest.testmod()
