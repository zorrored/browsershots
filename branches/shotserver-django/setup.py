from distutils.core import setup
import os
import sys

# Tell distutils to put data files next to Python files
# See http://groups.google.com/group/comp.lang.python/
# browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
from distutils.command.install import INSTALL_SCHEMES
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

root_dir = os.path.dirname(__file__)
lib_dir = os.path.join(root_dir, 'shotserver04')


def find_packages():
    for dirpath, dirnames, filenames in os.walk(lib_dir):
        for i, dirname in enumerate(dirnames):
            if dirname.startswith('.'):
                del dirnames[i]
        if '__init__.py' in filenames:
            yield dirpath[len(root_dir):].lstrip(os.sep).replace(os.sep, '.')


def find_data_files(data_dirnames=None):
    for dirpath, dirnames, filenames in os.walk(lib_dir):
        for i, dirname in enumerate(dirnames):
            if dirname.startswith('.'):
                del dirnames[i]
        if 'templates' in dirpath.split(os.sep):
            files = [os.path.join(dirpath, f) for f in filenames]
            if files:
                unified_path = os.path.join('shotserver04', 'templates')
                basename = os.path.basename(dirpath)
                if basename != 'templates':
                    unified_path = os.path.join(unified_path, basename)
                yield (unified_path, files)
        if (dirpath.endswith('/LC_MESSAGES') or
            dirpath.endswith('/static/css')):
            files = [os.path.join(dirpath, f) for f in filenames]
            yield (dirpath, files)


if sys.argv[1] == 'test':
    from pprint import pprint
    print 'root_dir:', repr(root_dir)
    print 'lib_dir:', repr(lib_dir)
    print 'packages:'
    pprint(list(find_packages()))
    print 'data_files:'
    pprint(list(find_data_files()))
    sys.exit(0)


setup(
    name = 'ShotServer',
    version = '0.4-alpha1',
    url = 'http://v04.browsershots.org/',
    author = 'Johann C. Rocholl',
    author_email = 'johann@browsershots.org',
    description = 'Test your web design in different browsers',
    packages = list(find_packages()),
    data_files = list(find_data_files()),
)
