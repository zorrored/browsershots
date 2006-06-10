#!/usr/bin/env python
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
Resize a number of screenshot images. Will create an output folder for
new width if necessary. Please make sure that the web server has read
and write permissions on the new files. Usage:
# resize.py <width> <filenames...>
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import sys, os

def zoom(filename, width):
    """
    Scale the PNG image given by the filename parameter to a new width.
    Save it with the same filename in a folder whose name is the new width.
    Skip existing files.
    """
    dest = "%d/%s" % (width, os.path.basename(filename))
    if os.path.isfile(dest):
        return

    command = "pngtopnm %s" % filename
    command += " | pnmscale -width %d" % width
    command += " | pnmtopng"
    command += " > %s" % dest
    print command
    result = os.system(command)
    if result:
        raise RuntimeError, "failed with exit code %d" % result

output_width = int(sys.argv[1])

if not os.path.isdir(str(output_width)):
    os.mkdir(str(output_width))

for input_filename in sys.argv[2:]:
    zoom(input_filename, output_width)
