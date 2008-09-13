# browsershots.org - Test your web design in different browsers
# Copyright (C) 2008 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Browsershots. If not, see <http://www.gnu.org/licenses/>.

"""
Helper functions for the factories app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import random
import base64
from datetime import datetime, timedelta
from django.db.models import Q

SECRET_KEY_DEFAULT_LENGTH = 512


def last_poll_timeout():
    """
    A screenshot factory is active if it polled after the timeout.
    """
    return datetime.now() - timedelta(minutes=10)


def random_secret_key(length=SECRET_KEY_DEFAULT_LENGTH):
    """
    Generate a random base64-encoded string.
    """
    assert length % 4 == 0
    random_chars = []
    for index in range(length / 4 * 3):
        if index % 23 == 0:
            random.seed()
        random_chars.append(chr(random.randint(0, 255)))
    return base64.b64encode(''.join(random_chars))


def jobs_for_factory(factory):
    """
    Get matching jobs for a factory configuration.
    """
    q = Q()
    for browser in factory.browser_set.filter(active=True):
        q |= Q(browser_name=browser.name,
               major=browser.major, minor=browser.minor)
