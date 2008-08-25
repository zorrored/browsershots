import time
import xmlrpclib
from django.test import TestCase
from django.test.client import Client

try:
    from hashlib import md5
except:
    from md5 import md5 # before Python 2.5


TESTCLIENT_PASSWORD = 'sha1$6efc0$f93efe9fd7542f25a7be94871ea45aa95de57161'
FACTORY1_SECRET = ''.join("""
xEcYUVx+3H4tFABMleVTm6DFd9NW1Z7cDJWQNnMWEP19jPrj0EMi8ux8Kp1uutiv
4Xf/UOLeOvpW3A5vX/0+aZT4B+ktsT+6j/50MjceG5bQY4pmVf1cg4JKqgl4FdOY
wd4d6DReY8uCXa8WUexiIuQvGdGHqk2wsBypVlnfZTZMHzHG4ivdufRXzgTE6+Ar
VbiQLrIXsvElzbkrETcqxefvtNX23cjTXqWZo7XoL5tk5u6d2pjEn/DM6JGWXtWx
ZaraPQpTaEZx5T8NGva0DDcFJewJH4jMTer9UqQOf57Ld73+XAz7U3AEm7lsezNQ
6hmq3MxgKJVm9zCdIIxQh0EmOLQkrmajw2pLM8JMoHxBoxvaQKe6TkxRBnkSIQVF
CMT326GQKUFzowhEZipydkp4myc7XctfyZ6gBIXUXHaRBd/4hYyF0i3XJX2cDMt9
5zbQncx+k44N4c+N/VKg2c8cOezIrtXcotKQ7Bxet2/u1ZGIEc2yR45f3iwwRqQ5
""".split())


class TestFile:

    def __init__(self, content):
        self.content = content
        self.index = 0

    def read(self, bytes):
        self.start = self.index
        self.index += bytes
        return self.content[self.start:self.index]

    def close(self):
        pass


class TestConnection:

    def __init__(self, client):
        self.client = client

    def getreply(self):
        if self.response.status_code / 100 == 2:
            return (self.response.status_code, 'OK', [])
        else:
            return (self.response.status_code, self.response.content, [])

    def getfile(self):
        return TestFile(self.response.content)


class TestTransport(xmlrpclib.Transport):

    def __init__(self, client):
        self.client = client

    def make_connection(self, host):
        return TestConnection(self.client)

    def send_request(self, connection, handler, request_body):
        pass

    def send_host(self, connection, host):
        pass

    def send_user_agent(self, connection):
        pass

    def send_content(self, connection, request_body):
        connection.response = self.client.post(
            '/xmlrpc/', request_body, 'text/xml')


class TestServerProxy(xmlrpclib.ServerProxy):

    def __init__(self, client):
        xmlrpclib.ServerProxy.__init__(
            self, 'http://localhost/xmlrpc/',
            TestTransport(client))


def authenticate(method_name, args, secret):
    args.append(time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    message = ' '.join([method_name] + [str(arg) for arg in args] + [secret])
    args.append(md5(message).hexdigest())


class XMLRPCTestCase(TestCase):
    fixtures = ['authtestdata', 'test_factories']

    def setUp(self):
        self.server = TestServerProxy(self.client)

    def testUserAuth(self):
        args = ['testclient', 123, 'hello']
        authenticate('users.testAuth', args, TESTCLIENT_PASSWORD)
        self.assertEquals(self.server.users.testAuth(*args), 'OK')

    def testFactoryAuth(self):
        args = ['factory1', 123, 'hello']
        authenticate('factories.testAuth', args, FACTORY1_SECRET)
        self.assertEquals(self.server.factories.testAuth(*args), 'OK')
