import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'shotserver04.settings'
from datetime import datetime, timedelta
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser
from shotserver04.screenshots.models import Screenshot

ONE_HOUR_AGO = datetime.now() - timedelta(0, 3600, 0)
ONE_DAY_AGO = datetime.now() - timedelta(1, 0, 0)

for factory in Factory.objects.all():
    factory.uploads_per_hour = Screenshot.objects.filter(
        factory=factory, uploaded__gte=ONE_HOUR_AGO).count()
    factory.uploads_per_day = Screenshot.objects.filter(
        factory=factory, uploaded__gte=ONE_DAY_AGO).count()
    factory.save()

for browser in Browser.objects.all():
    browser.uploads_per_hour = Screenshot.objects.filter(
        browser=browser, uploaded__gte=ONE_HOUR_AGO).count()
    browser.uploads_per_day = Screenshot.objects.filter(
        browser=browser, uploaded__gte=ONE_DAY_AGO).count()
    browser.save()
