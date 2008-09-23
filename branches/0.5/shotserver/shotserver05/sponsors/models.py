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
Models for the sponsors app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.db import models
from django.contrib.auth.models import User


class Sponsor(models.Model):
    """
    Sponsors support the project by running screenshot factories or
    with donations.
    """
    user = models.ForeignKey(User)
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)
