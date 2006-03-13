from distutils.core import setup

setup(name = 'ShotServer',
      version = '0.3.0',
      description = 'Server software for browsershots.org',
      author = 'Johann C. Rocholl',
      author_email = 'johann@browsershots.org',
      url = 'http://browsershots.org/',
      package_dir = {'shotserver03': 'lib'},
      packages = ['shotserver03',
                  'shotserver03.actions',
                  'shotserver03.database',
                  'shotserver03.interface'],
      scripts = ['scripts/shotserver03_db_create.py'],
      data_files = [('shotserver03/style', ['style/style.css'])],
      )
