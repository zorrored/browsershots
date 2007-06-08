import re
import os
import tempfile
from xmlrpclib import Fault
from shotserver04 import settings
from shotserver04.nonces import crypto

ORIGINAL_SIZE = 'original'
HEADER_MATCH = re.compile(r'(\S\S)\s+(\d+)\s+(\d+)\s+').match


def png_path(hashkey, size=ORIGINAL_SIZE):
    return os.path.join(settings.PNG_ROOT, str(size), hashkey[:2])


def png_filename(hashkey, size=ORIGINAL_SIZE):
    return os.path.join(png_path(hashkey, size), hashkey + '.png')


def makedirs(path):
    if os.path.exists(path):
        return
    try:
        os.makedirs(path)
    except OSError, error:
        raise Fault(0, error)


def save_upload(screenshot):
    hashkey = crypto.random_md5()
    makedirs(png_path(hashkey))
    try:
        outfile = file(png_filename(hashkey), 'wb')
        outfile.write(screenshot.data)
        outfile.close()
    except IOError, error:
        raise Fault(0, error)
    return hashkey


def pngtoppm(hashkey):
    pngname = png_filename(hashkey)
    ppmhandle, ppmname = tempfile.mkstemp()
    os.close(ppmhandle)
    error = os.system('pngtopnm "%s" > "%s"' % (pngname, ppmname))
    if error:
        makedirs(png_path(hashkey, 'error'))
        errorname = png_filename(hashkey, 'error')
        os.system('mv "%s" "%s"' % (pngname, errorname))
        raise Fault(0,
            'Could not decode uploaded PNG file (hashkey %s).' % hashkey)
    if not os.path.exists(ppmname):
        raise Fault(0, 'Decoded screenshot file not found.')
    if os.path.getsize(ppmname) == 0:
        raise Fault(0, 'Decoded screenshot file is empty.')
    return ppmname


def read_pnm_header(ppmname):
    header = file(ppmname, 'rb').read(1024)
    match = HEADER_MATCH(header)
    if match is None:
        raise Fault(0,
            'Could not read PNM header after decoding uploaded PNG file.')
    return (
        match.group(1),
        int(match.group(2)),
        int(match.group(3)),
        )


def scale(ppmname, width, hashkey):
    makedirs(png_path(hashkey, size=width))
    pngname = png_filename(hashkey, size=width)
    error = os.system('pnmscale -width=%d "%s" | pnmtopng > %s' %
                      (width, ppmname, pngname))
    if error:
        raise Fault(0,
            "Could not create scaled preview image.")
