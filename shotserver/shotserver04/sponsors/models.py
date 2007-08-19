# browsershots.org - Test your web design in different browsers
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
Sponsors for screenshot factories.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.db import models


class Sponsor(models.Model):
    """
    Show sponsor links near screenshots from sponsored factories.
    """

    name = models.CharField(
        _('name'), max_length=50)
    slug = models.SlugField(
        _('slug'), max_length=50, prepopulate_from=('name', ),
        help_text=_("This is used to generate the link to the logo image."))
    url = models.URLField(
        _('URL'), max_length=400, unique=True, verify_exists=False)
    premium = models.BooleanField(
        _('premium'),
        help_text=_("Premium sponsors are shown on the front page."))

    class Admin:
        list_display = ('name', 'slug', 'url', 'premium')

    class Meta:
        verbose_name = _('sponsor')
        verbose_name_plural = _('sponsors')
        ordering = ('name', )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        """Get redirect URL for sponsor links."""
        return '/sponsors/%s/' % self.slug

    def get_logo_url(self, size=(234, 60)):
        """Get absolute URL of logo image."""
        return '/static/logos/%dx%d/%s.png' % (size[0], size[1], self.slug)

    def logo(self, size=(234, 60)):
        """Get HTML image with link to sponsor website."""
        img = '<img width="%d" height="%d" src="%s" alt="%s" />' % (
            size[0], size[1], self.get_logo_url(size), self.name)
        return '<a href="%s">%s</a>' % (self.get_absolute_url(), img)
