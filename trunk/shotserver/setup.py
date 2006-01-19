#! /usr/bin/env python

from distutils.core import setup

setup(name = 'ShotServer',
      version = '0.3.0',
      description = 'Server software for browsershots.org',
      author = 'Johann C. Rocholl',
      author_email = 'johann@browsershots.org',
      url = 'http://browsershots.org/',
      package_dir = {'shotserver': 'lib'},
      packages = ['shotserver'],
      scripts = ['scripts/shotserver_db_create.py'],
      )
