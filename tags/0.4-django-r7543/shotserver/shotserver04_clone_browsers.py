#!/usr/bin/env python

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'shotserver04.settings'

import sys
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser

source = Factory.objects.get(name=sys.argv[1])
dest, created = Factory.objects.get_or_create(
    name=sys.argv[2],
    defaults={
        'admin_id': source.admin_id,
        'sponsor_id': source.sponsor_id,
        'operating_system_id': source.operating_system_id,
        'ip': source.ip,
        'hardware': source.hardware,
        })

source_browsers = source.browser_set.filter(active=True)
active_dest_browser_ids = []
for source_browser in source_browsers:
    settings = {
        'browser_group_id': source_browser.browser_group_id,
        'version': source_browser.version,
        'major': source_browser.major,
        'minor': source_browser.minor,
        'engine_id': source_browser.engine_id,
        'engine_version': source_browser.engine_version,
        'javascript_id': source_browser.javascript_id,
        'java_id': source_browser.java_id,
        'flash_id': source_browser.flash_id,
        'command': source_browser.command,
        'active': True,
        }
    dest_browser, created = Browser.objects.get_or_create(
        factory=dest,
        user_agent=source_browser.user_agent,
        defaults=settings)
    if not created:
        for key in list(settings.keys()):
            if key.endswith('_id'):
                new_key = key[:-3]
                settings[new_key] = settings[key]
                del(settings[key])
        dest_browser.update_fields(**settings)
    active_dest_browser_ids.append(dest_browser.id)


# Deactivate all other browsers on destination
for browser in dest.browser_set.filter(active=True):
    if browser.id not in active_dest_browser_ids:
        browser.update_fields(active=False)
