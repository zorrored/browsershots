from shotserver05.xmlrpc.utils import signature, user_auth, factory_auth

@user_auth
@signature(str, int, str)
def testAuth(request, user, dummy_number, dummy_text):
    return 'OK'
