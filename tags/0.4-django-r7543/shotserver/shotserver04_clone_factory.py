#!/usr/bin/env python

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'shotserver04.settings'

import sys
from shotserver04.factories.models import Factory

source = Factory.objects.get(name=sys.argv[1])
dest = Factory.objects.create(
    name=sys.argv[2],
    admin_id=source.admin_id,
    sponsor_id=source.sponsor_id,
    operating_system_id=source.operating_system_id,
    ip=source.ip,
    hardware=source.hardware,
    )
