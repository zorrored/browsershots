from shotserver05.xmlrpc.utils import user_auth


@user_auth
def testAuth(request, user, dummy_number, dummy_text):
    """
    Test user authentication with MD5 hash. To compute the hash,
    concatenate the string values of all the other arguments and the
    pre-hashed user password, then get the MD5 hash as 32 lowercase
    hexadecimal characters.

    Arguments:
    * dummy_number int (e.g. 123)
    * dummy_text string (e.g. hello)

    If the username is 'joe' and the pre-hashed password is
    'sha1$e3$4d07f85', you might get the following MD5 hash:

    >>> md5('123hello2008-08-08T23:56:14Zjoesha1$e3$4d07f85').hexdigest()
    '2eb594e041eeb418e86ef0289328ed1c'

    Return value:
    * status string (OK)
    """
    return 'OK'
