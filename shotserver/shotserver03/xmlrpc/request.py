# browsershots.org ShotServer 0.3-beta1
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.

"""
Screenshot request handling.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import os
import tempfile
import re
from shotserver03.util import md5nonce
from shotserver03 import database

export_methods = ['poll', 'upload']
pngpath = '/var/www/browsershots.org/png'
min_upload_kilobytes = 10


def poll(factory, crypt):
    """
    poll(string, string) => array
    Try to find a matching screenshot request for a given factory.

    Arguments:
        factory -- the name of the factory (string, length max 20)
        crypt -- crypted password (hex string, length 32)

    Return value:
        status -- 'OK' or error message
        challenge -- random authentication challenge (salt + nonce)
        options -- dictionary with requested configuration

    If successful, the request will be locked for 3 minutes. This is
    to make sure that no requests are processed by two factories at
    the same time. If your factory takes longer to process a request,
    it is possible that somebody else will lock it. In this case, your
    upload will fail.

    The challenge consists of a salt (4 characters) and a nonce (32
    characters). The password is encrypted with MD5 as follows:
    crypt = md5(md5(salt + password) + nonce)

    If successful, options contains the following keys:
        browser -- browser name
        width -- screen width in pixels
        bpp -- color depth (bits per pixel)
        js -- javascript version string
        java -- java version string
        flash -- flash version string
        media -- media player string
        binary -- browser command to run

    """
    database.connect()
    try:
        if factory == 'disabled':
            sorry = ' '.join((
                "Sorry, your factory is disabled.",
                "Please check your mail.",
                ))
            return sorry, '', {}
        factory = database.factory.name_to_serial(factory)
        ip = req.connection.remote_ip
        status = database.nonce.authenticate_factory(factory, ip, crypt)
        if status != 'OK':
            return status, '', {}
        database.factory.update_last_poll(factory)
        where = database.factory.features(factory)
        if where.count('()'):
            return 'Factory configuration incomplete.', '', {}
        # Find the oldest non-expired request.
        row = database.request.select_match(where
            + " AND request_group.expire >= NOW()")
        if row is None:
            # Find the youngest expired request.
            row = database.request.select_match(where
                + " AND request_group.created >= NOW()-'4:00'::interval",
                'DESC')
        if row is None:
            return 'No matching request.', '', {}
        else:
            request = row[0]
            database.request.update_locked(request, factory)
            salt = database.factory.select_salt(factory)
            nonce = database.nonce.create_request_nonce(request, ip)
            challenge = salt + nonce
            options = database.request.to_dict(row)
            options['command'] = database.factory_browser.get_command(factory,
                options['browser'], options['major'], options['minor'])
            return 'OK', challenge, options
    finally:
        database.disconnect()


header_match = re.compile(r'(P\d) (\d+) (\d+) (\d+)').match


def read_ppm_header(infile):
    """
    Read a PPM file header and return magic, width, height, maxval.
    """
    header = []
    while True:
        line = infile.readline()
        sharp = line.find('#')
        if sharp > -1:
            line = line[:sharp]
        line = line.strip()
        if not line:
            continue
        header.append(line)
        match = header_match(' '.join(header))
        if match:
            magic = match.group(1)
            width = int(match.group(2))
            height = int(match.group(3))
            maxval = int(match.group(4))
            return magic, width, height, maxval
        elif len(header) >= 4:
            raise SyntaxError("could not parse PPM header")


def save_upload(binary, hashkey):
    """
    Save the upload to a PNG file.
    """
    prefix = hashkey[:2]
    fullpath = '%s/full/%s' % (pngpath, prefix)
    if not os.path.exists(fullpath):
        os.makedirs(fullpath)
    pngname = '%s/%s.png' % (fullpath, hashkey)
    outfile = file(pngname, 'wb')
    outfile.write(binary.data)
    outfile.close()


def pngtoppm(hashkey):
    """
    Decode the uploaded PNG file to a temporary PPM.
    """
    prefix = hashkey[:2]
    fullpath = '%s/full/%s' % (pngpath, prefix)
    pngname = '%s/%s.png' % (fullpath, hashkey)
    ppmhandle, ppmname = tempfile.mkstemp()
    os.close(ppmhandle)
    error = os.system('pngtopnm "%s" > "%s"' % (pngname, ppmname))
    if error:
        errorpath = '%s/error/%s' % (pngpath, prefix)
        if not os.path.exists(errorpath):
            os.makedirs(errorpath)
        errorname = '%s/%s.png' % (errorpath, hashkey)
        os.system('mv %s %s' % (pngname, errorname))
        return ('Could not decode uploaded PNG file (hashkey %s).' % hashkey,
                0, 0, 0, '')
    magic, width, height, maxval = read_ppm_header(file(ppmname))
    assert magic == 'P6'
    assert maxval == 255
    return 'OK', width, height, ppmname


def zoom(ppmname, hashkey, width):
    """
    Make smaller preview images.
    """
    prefix = hashkey[:2]
    zoompath = '%s/%d/%s' % (pngpath, width, prefix)
    if not os.path.exists(zoompath):
        os.makedirs(zoompath)
    pngname = '%s/%s.png' % (zoompath, hashkey)
    error = os.system('pnmscalefixed -width %d "%s" | pnmtopng > "%s"'
                      % (width, ppmname, pngname))
    return not error


def upload(binary, crypt):
    """
    upload(binary, string) => array
    Upload a browser screenshot.

    Arguments:
    screenshot -- a PNG file (base64 encoded binary data)
    crypt -- crypted password (hex string, length 32)

    Return value:
    status -- 'OK' or error message
    challenge -- random authentication challenge (salt + nonce)
    """
    database.connect()
    ppmname = ''
    try:
        ip = req.connection.remote_ip
        status, request, request_width, factory, factory_browser = \
            database.nonce.authenticate_request(ip, crypt)
        if status != 'OK':
            return status, ''
        if factory_browser is None:
            return "The browser has not visited the requested URL.", ''

        if len(binary.data) < min_upload_kilobytes * 1024:
            return ("The uploaded screenshot is too small (less than %d KB)." %
                    min_upload_kilobytes, '')

        hashkey = md5nonce.random_md5()
        save_upload(binary, hashkey)

        status, width, height, ppmname = pngtoppm(hashkey)
        if status != 'OK':
            return status, ''
        if request_width is not None and width != request_width:
            return ("Uploaded image width (%d) is not as requested (%d)."
                    % (width, request_width)), ''
        if height > database.options.max_screenshot_height:
            return ("Uploaded image height (%d) is greater than maximum (%d)."
                    % (height, database.options.max_screenshot_height)), ''

        assert zoom(ppmname, hashkey, 140) # 5*140 + 4*16 = 764
        assert zoom(ppmname, hashkey, 180) # 4*180 + 3*14 = 762
        assert zoom(ppmname, hashkey, 240) # 3*240 + 2*22 = 764
        assert zoom(ppmname, hashkey, 450) # 3*140 + 2*15

        database.screenshot.insert(
            hashkey, factory, factory_browser, width, height)
        database.request.update_screenshot(request, database.lastval())
        database.factory.update_last_upload(factory)
        database.factory_browser.update_last_upload(factory_browser)

        salt = database.factory.select_salt(factory)
        nonce = database.nonce.create_factory_nonce(factory, ip)
        challenge = salt + nonce
        return 'OK', challenge
    finally:
        if os.path.exists(ppmname):
            os.unlink(ppmname)
        database.disconnect()
