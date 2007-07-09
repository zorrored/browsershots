def split_netloc(netloc):
    """
    Split network locator into username, password, hostname, port.

    >>> split_netloc('example.com')
    (None, None, 'example.com', None)
    >>> split_netloc('user@example.com')
    ('user', None, 'example.com', None)
    >>> split_netloc('user:pw@example.com:80')
    ('user', 'pw', 'example.com', '80')
    """
    auth = username = password = None
    host = hostname = port = None
    if '@' in netloc:
        auth, host = netloc.split('@', 1)
    else:
        host = netloc
    if auth and ':' in auth:
        username, password = auth.split(':', 1)
    else:
        username = auth
    if host and ':' in host:
        hostname, port = host.split(':', 1)
    else:
        hostname = host
    return username, password, hostname, port


if __name__ == '__main__':
    import doctest
    doctest.testmod()
