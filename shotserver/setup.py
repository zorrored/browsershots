# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name = 'ShotServer',
      version = '0.3.0',
      description = 'Server software for browsershots.org',
      author = 'Johann C. Rocholl',
      author_email = 'johann@browsershots.org',
      url = 'http://browsershots.org/',
      package_dir = {'shotserver03': 'lib'},
      packages = [
            'shotserver03',
            'shotserver03.get',
            'shotserver03.post',
            'shotserver03.database',
            'shotserver03.interface',
            'shotserver03.request',
            'shotserver03.segments',
            'shotserver03.xmlrpc',
            ],
      scripts = [
            'scripts/shotserver03_db_drop_create.sh',
            'scripts/shotserver03_resize.py',
            'scripts/shotserver03_db_backup.sh',
            'scripts/svn_backup.py',
            ],
      data_files = [
            ('share/shotserver03/style', [
                  'style/style.css',
                  'style/logo40.png',
                  'style/mfg40.png',
                  'style/lisog40.png',
                  'style/blue.jpg',
                  'style/gray.jpg',
                  'style/zoom.js',
                  'style/forms.js',
                  ])],
      )
