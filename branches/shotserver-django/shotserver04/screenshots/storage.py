import os
import tempfile
from shotserver04 import settings
from shotserver04.nonces import crypto


def png_path(hashkey, size='full'):
    return os.path.join(settings.PNG_ROOT, size, hashkey[:2])


def png_filename(hashkey, size='full'):
    return os.path.join(settings.PNG_ROOT, size, hashkey[:2], hashkey + '.png')


def save_upload(screenshot):
    hashkey = crypto.random_md5()
    fullpath = png_path(hashkey)
    if not os.path.exists(fullpath):
        try:
            os.makedirs(fullpath)
        except OSError, error:
            raise ErrorMessage(error)
    pngname = png_filename(hashkey)
    try:
        outfile = file(pngname, 'wb')
    except IOError, error:
        raise ErrorMessage(error)
    outfile.write(screenshot.data)
    outfile.close()
    return hashkey


def pngtoppm(hashkey):
    pngname = png_filename(hashkey)
    ppmhandle, ppmname = tempfile.mkstemp()
    os.close(ppmhandle)
    error = os.system('pngtopnm "%s" > "%s"' % (pngname, ppmname))
    if error:
        errorpath = png_path(hashkey, 'error')
        if not os.path.exists(errorpath):
            os.makedirs(errorpath)
        errorname = png_filename(hashkey, 'error')
        os.system('mv "%s" "%s"' % (pngname, errorname))
        raise ErrorMessage(
            'Could not decode uploaded PNG file (hashkey %s).' % hashkey)
    return ppmname
