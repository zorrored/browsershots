from psycopg import IntegrityError, ProgrammingError
from unittest import TestCase
from django.db import transaction
from django.contrib.auth.models import User
from shotserver04.platforms.models import Architecture
from shotserver04.platforms.models import Platform, OperatingSystem
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Engine, BrowserGroup, Browser


class SizeTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.architecture = Architecture.objects.create()
        self.platform = Platform.objects.create()
        self.operating_system = OperatingSystem.objects.create(
            platform=self.platform)
        self.factory = Factory.objects.create(
            name='factory',
            admin=self.user,
            architecture=self.architecture,
            operating_system=self.operating_system)
        self.engine = Engine.objects.create(
            name='Gecko', maker='Mozilla')
        self.browser_group = BrowserGroup.objects.create(
            name='Firefox', maker='Mozilla', terminal=False)

    def tearDown(self):
        self.browser_group.delete()
        self.engine.delete()
        self.factory.delete()
        self.operating_system.delete()
        self.platform.delete()
        self.architecture.delete()
        self.user.delete()

    def createBrowser(self, user_agent, **kwargs):
        return Browser.objects.create(
            factory=self.factory,
            user_agent=user_agent,
            browser_group=self.browser_group,
            version=kwargs.get('version', ''),
            major=kwargs.get('major', 0),
            minor=kwargs.get('minor', 0),
            engine=self.engine,
            engine_version=kwargs.get('engine_version', ''),
            javascript=kwargs.get('javascript', ''),
            java=kwargs.get('java', ''),
            flash=kwargs.get('flash', ''),
            command=kwargs.get('command', ''),
            disabled=kwargs.get('disabled', False),
            )

    def assertBrowserValid(self, user_agent, **kwargs):
        try:
            self.createBrowser(user_agent, **kwargs).delete()
        except (IntegrityError, ProgrammingError):
            transaction.rollback()
            self.fail('\n'.join((
                "could not create browser with valid settings:",
                '"%s"' % user_agent, repr(kwargs))))

    def assertBrowserInvalid(self, user_agent, **kwargs):
        try:
            try:
                self.createBrowser(user_agent, **kwargs).delete()
                self.fail('\n'.join((
                    "created browser with invalid settings:",
                    '"%s"' % user_agent, repr(kwargs))))
            except IntegrityError:
                pass
        finally:
            transaction.rollback()

    def testFirefox15(self):
        self.assertBrowserValid('Firefox/1.5.0.8',
                                version='1.5.0.8', major=1, minor=5)

    def testFirefox20(self):
        self.assertBrowserValid('Firefox/2.0.0.1',
                                version='2.0.0.1', major=2, minor=0)

    def testGecko(self):
        self.assertBrowserValid('Gecko/20061226 Firefox/2.0.0.1',
                                version='2.0.0.1', major=2, minor=0,
                                engine_version='20061226')

    def testBogusVersion(self):
        self.assertBrowserInvalid('Firefox/2.0.0.1',
                                  version='2.0.0.2', major=2, minor=0)

    def testBogusMajor(self):
        self.assertBrowserInvalid('Firefox/2.0.0.1',
                                  version='2.0.0.1', major=1, minor=0)

    def testBogusMinor(self):
        self.assertBrowserInvalid('Firefox/2.0.0.1',
                                  version='2.0.0.1', major=2, minor=1)

    def testBogusMajorMinor(self):
        self.assertBrowserInvalid('Firefox/2.0.0.1',
                                  version='2.0.0.1', major=0, minor=1)

    def testBogusEngine(self):
        self.assertBrowserInvalid('Gecko/20061226 Firefox/2.0.0.1',
                                  version='2.0.0.1', major=2, minor=0,
                                  engine_version='20061220')
