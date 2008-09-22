# browsershots.org - Test your web design in different browsers
# Copyright (C) 2008 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Browsershots. If not, see <http://www.gnu.org/licenses/>.

"""
Tests for the accounts app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import re
from django.test import TestCase
from django.core import mail
from shotserver05.xmlrpc.tests import TestServerProxy, authenticate
from shotserver05.system.utils import signature

TESTCLIENT_PASSWORD = 'sha1$6efc0$f93efe9fd7542f25a7be94871ea45aa95de57161'


class AccountsTestCase(TestCase):
    fixtures = ['authtestdata']

    def testLogin(self):
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 302)
        self.assert_('/accounts/login/' in response['Location'])
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assert_('id_username' in response.content)
        self.assert_('id_password' in response.content)
        response = self.client.post('/accounts/login/',
            {'username': 'testclient', 'password': 'password'})
        self.assertEqual(response.status_code, 302)
        self.assert_(response['Location'].endswith('/accounts/profile/'))
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)

    def testLogout(self):
        self.client.login(username='testclient', password='password')
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)
        self.assert_('logged out' in response.content.lower())
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 302)
        self.assert_('/accounts/login/' in response['Location'])

    def testCreate(self):
        path = '/accounts/create/'
        response = self.client.post(path, {'first_name': 'joe'})
        self.assert_('must start with uppercase' in response.content)
        response = self.client.post(path, {'last_name': 'schmoe'})
        self.assert_('must start with uppercase' in response.content)
        response = self.client.post(path, {'username': '123'})
        self.assert_('username must match' in response.content.lower())
        response = self.client.post(path, {'password': '123'})
        self.assert_('at least 6 characters' in response.content)
        response = self.client.post(path, {'password': '123456'})
        self.assert_('too simple' in response.content)
        response = self.client.post(path,
            {'first_name': 'Joe', 'last_name': 'Schmoe', 'username': 'joe',
             'password': 'test123', 'repeat': 'test123',
             'email': 'joe@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assert_('account created' in response.content.lower())

    def testCreateValidate(self):
        response = self.client.post('/accounts/create/validate/username/',
            {'username': 'testclient'})
        self.assertEqual(response.status_code, 200)
        self.assert_('reserved' in response.content.lower())

    def testPasswordChange(self):
        response = self.client.get('/accounts/password/change/')
        self.assertEqual(response.status_code, 302)
        self.assert_(response['Location'].endswith, '/accounts/login/' +
                     '?next=/accounts/password/change/')
        response = self.client.post('/accounts/password/change/',
                                    {'old_password': 'password',
                                     'new_password1': 'newpassword',
                                     'new_password2': 'newpassword'})
        self.assertEqual(response.status_code, 302)
        self.assert_(response['Location'].endswith, '/accounts/login/' +
                     '?next=/accounts/password/change/')
        # Log in and try again
        self.client.login(username='testclient', password='password')
        response = self.client.get('/accounts/password/change/')
        self.assertEqual(response.status_code, 200)
        self.assert_('id_old_password' in response.content)
        response = self.client.post('/accounts/password/change/',
                                    {'old_password': 'password',
                                     'new_password1': 'newpassword',
                                     'new_password2': 'newpassword'})
        self.assertEqual(response.status_code, 302)
        self.assert_(response['Location'].endswith,
                     '/accounts/password/change/done/')

    def testPasswordReset(self):
        self.assertEquals(len(mail.outbox), 0)
        response = self.client.get('/accounts/password/reset/')
        self.assertEqual(response.status_code, 200)
        self.assert_('id_email' in response.content)
        response = self.client.post('/accounts/password/reset/',
                                    {'email': 'staffmember@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assert_(response['Location'].endswith,
                     '/accounts/password/reset/done/')
        self.assertEquals(len(mail.outbox), 1)
        body = mail.outbox[0].body
        match = re.search('/accounts/password/reset/confirm/\S+', body)
        self.assert_(match is not None)
        path = match.group()
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assert_('reset' in response.content)
        response = self.client.post(path,
                                    {'new_password1': 'newpassword',
                                     'new_password2': 'newpassword'})
        self.assertEqual(response.status_code, 302)
        self.assert_(response['Location'].endswith,
                     '/accounts/password/reset/complete/')


class XMLRPCTestCase(TestCase):
    fixtures = ['authtestdata']

    def setUp(self):
        self.server = TestServerProxy(self.client)

    def testAuth(self):
        self.assertEqual(
            signature('accounts.testAuth'),
            ['string', 'string', 'int', 'string', 'string', 'string'])
        args = ['testclient', 123, 'hello']
        authenticate('accounts.testAuth', args, TESTCLIENT_PASSWORD)
        self.assertEquals(self.server.accounts.testAuth(*args), 'OK')
