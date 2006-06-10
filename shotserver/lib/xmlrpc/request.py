# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Screenshot request handling.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import os, tempfile
from shotserver03 import database

export_methods = ['poll', 'upload']

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
        browser -- browser name, possibly with version number
        width -- screen width in pixels
        bpp -- color depth (bits per pixel)
        js -- javascript version string
        java -- java version string
        flash -- flash version string
        media -- media player string

    """
    database.connect()
    try:
        factory = database.factory.select_serial(factory)
        ip = req.connection.remote_ip
        status = database.nonce.authenticate_factory(factory, ip, crypt)
        if status != 'OK':
            return status, '', {}
        where = database.factory.features(factory)
        row = database.request.match(where)
        if row is None:
            return 'No matching request.', '', {}
        else:
            request = row[0]
            database.lock.attempt(factory, request)
            salt = database.factory.select_salt(factory)
            nonce = database.nonce.create_request_nonce(request, ip)
            options = database.request.to_dict(row)
            challenge = salt + nonce
            return 'OK', challenge, options
    finally:
        database.disconnect()

def zoom(ppmname, pngpath, prefix, hashkey, width):
    """
    Make smaller preview images.
    """
    zoompath = '%s/%d/%s' % (pngpath, width, prefix)
    if not os.path.exists(zoompath):
        os.makedirs(zoompath)
    pngname = '%s/%s.png' % (zoompath, hashkey)
    error = os.system('pnmscalefixed -width %d "%s" | pnmtopng > "%s"'
                      % (width, ppmname, pngname))
    return not error

def upload(binary, crypt):
    """
    Upload a browser screenshot.
    """
    pngpath = '/var/www/browsershots.org/png'
    database.connect()
    try:
        ip = req.connection.remote_ip
        status, request = database.nonce.authenticate_request(ip, crypt)
        if status != 'OK':
            return status

        hashkey = database.nonce.random_md5()
        prefix = hashkey[:2]
        fullpath = '%s/full/%s' % (pngpath, prefix)
        if not os.path.exists(fullpath):
            os.makedirs(fullpath)
        pngname = '%s/%s.png' % (fullpath, hashkey)
        outfile = file(pngname, 'wb')
        outfile.write(binary.data)
        outfile.close()

        ppmhandle, ppmname = tempfile.mkstemp()
        error = os.system('pngtopnm "%s" > "%s"' % (pngname, ppmname))
        assert not error
        assert zoom(ppmname, pngpath, prefix, hashkey, 200)
        assert zoom(ppmname, pngpath, prefix, hashkey, 400)
        os.close(ppmhandle)
        os.unlink(ppmname)
        return 'OK'
    finally:
        database.disconnect()
