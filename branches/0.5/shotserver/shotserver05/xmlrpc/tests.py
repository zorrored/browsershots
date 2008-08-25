import time
import xmlrpclib

try:
    from hashlib import md5
except:
    from md5 import md5 # before Python 2.5


def authenticate(method_name, args, secret):
    args.append(time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    message = ' '.join([method_name] + [str(arg) for arg in args] + [secret])
    args.append(md5(message).hexdigest())


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
