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
Explain the purpose of this project.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml

def write():
    """
    Write XHTML div with a quick project introduction.
    """
    xhtml.write_open_tag_line('div', _id="about")
    xhtml.write_tag_line('h2', "What is this?")

    text = ("Browsershots is a free online platform where you can test your web design in different browsers.",
            "When you submit your web address, it will be added to the job queue.",
            "A number of distributed computers will automatically open your website in their browser.",
            "Then they will make screenshots and upload them to the central server here.")
    text = '\n'.join(text)
    xhtml.write_tag_line('p', text)

    xhtml.write_close_tag_line('div') # id="about"
