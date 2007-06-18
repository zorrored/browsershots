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
Screenshot models.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import os
from django.db import models, backend
from django.utils.translation import gettext_lazy as _
from django.utils.text import capfirst
from shotserver04.websites.models import Website
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser
from shotserver04.screenshots import storage


class ScreenshotManager(models.Manager):

    def _quote(self, name):
        return '%s.%s' % (
            backend.quote_name(self.model._meta.db_table),
            backend.quote_name(name))

    def recent(self):
        """
        Get recent screenshots, but only one per website.
        """
        from django.db import connection
        cursor = connection.cursor()
        fields = ','.join(
            [self._quote(field.column) for field in self.model._meta.fields])
        cursor.execute("""
            SELECT """ + fields + """
            FROM """ + backend.quote_name(self.model._meta.db_table) + """
            WHERE """ + self._quote('id') + """ IN (
                SELECT MAX(""" + self._quote('id') + """)
                AS """ + backend.quote_name('maximum') + """
                FROM  """ + backend.quote_name(self.model._meta.db_table) + """
                GROUP BY """ + self._quote('website_id') + """
                ORDER BY """ + backend.quote_name('maximum') + """ DESC
                LIMIT 100)
            ORDER BY """ + self._quote('id') + """ DESC
            """)
        for row in cursor.fetchall():
            yield self.model(*row)


class Screenshot(models.Model):
    hashkey = models.SlugField(
        _('hashkey'), maxlength=32, unique=True)
    website = models.ForeignKey(Website,
        verbose_name=_('website'), raw_id_admin=True)
    factory = models.ForeignKey(Factory,
        verbose_name=_('factory'), raw_id_admin=True)
    browser = models.ForeignKey(Browser,
        verbose_name=_('browser'), raw_id_admin=True)
    width = models.IntegerField(
        _('width'))
    height = models.IntegerField(
        _('height'))
    uploaded = models.DateTimeField(
        _('uploaded'), auto_now_add=True)
    objects = ScreenshotManager()

    class Admin:
        fields = (
            (None, {'fields': (
            'hashkey',
            ('website', 'factory', 'browser'),
            ('width', 'height'),
            'uploaded',
            )}),
            )
        list_display = ('hashkey', 'factory', 'browser',
                        'width', 'height', 'uploaded')

    class Meta:
        verbose_name = _('screenshot')
        verbose_name_plural = _('screenshots')
        ordering = ('uploaded', )

    def __str__(self):
        return self.hashkey

    def get_absolute_url(self):
        return '/screenshots/%s/' % self.hashkey

    def get_size_url(self, size='original'):
        return '/png/%s/%s/%s.png' % (size, self.hashkey[:2], self.hashkey)

    def get_large_url(self):
        return self.get_size_url(size=512)

    def preview_img(self, width=160, title=None):
        height = self.height * width / self.width
        style = 'width:%spx;height:%spx;z-index:0' % (width / 2, height / 2)
        if title is None:
            title = str(self.browser)
        return ' '.join((
            '<img class="preview" style="%s"' % style,
            'src="%s"' % self.get_size_url(width),
            'alt="%s" title="%s"' % (title, title),
            'onmouseover="larger(this,%s,%s)"' % (width, height),
            'onmouseout="smaller(this,%s,%s)" />' % (width, height),
            ))

    def preview_div(self, width=80, title=None, style="float:left"):
        height = self.height * width / self.width
        style = 'width:%dpx;height:%dpx;%s' % (width, height, style)
        return ''.join((
            '<div class="preview" style="%s">' % style,
            '<a href="%s">' % self.get_absolute_url(),
            self.preview_img(width=2*width, title=title),
            '</a></div>',
            ))

    def get_file_size(self):
        """Get size in bytes of original screenshot file."""
        return os.path.getsize(storage.png_filename(self.hashkey))

    def link(self, text=None, div_class='screenshot-link'):
        if text is None:
            text = str(self)
        return ' '.join((
            '<div class="%s">' % div_class,
            '<a href="%s">%s</a>' % (self.get_absolute_url(), text),
            '</div>',
            ))

    def arrow(self, screenshot, img, alt):
        if not screenshot:
            return '<img src="/static/css/%s-gray.png" alt="%s">' % (img, alt)
        return ''.join((
            '<a href="%s">' % screenshot.get_absolute_url(),
            '<img src="/static/css/%s.png" alt="%s">' % (img, alt),
            '</a>',
            ))

    def get_first(self, **kwargs):
        return Screenshot.objects.filter(**kwargs).order_by('id')[:1]

    def get_last(self, **kwargs):
        return Screenshot.objects.filter(**kwargs).order_by('-id')[:1]

    def get_previous(self, **kwargs):
        return Screenshot.objects.filter(
            id__lt=self.id, **kwargs).order_by('-id')[:1]

    def get_next(self, **kwargs):
        return Screenshot.objects.filter(
            id__gt=self.id, **kwargs).order_by('id')[:1]

    def not_me(self, screenshots):
        if screenshots and screenshots[0] != self:
            return screenshots[0]

    def arrows(self, **kwargs):
        """
        Show links for related screenshots.
        """
        first = self.not_me(self.get_first(**kwargs))
        previous = self.not_me(self.get_previous(**kwargs))
        next = self.not_me(self.get_next(**kwargs))
        last = self.not_me(self.get_last(**kwargs))
        return '\n'.join((
            self.arrow(first, 'first', capfirst(_("first"))),
            self.arrow(previous, 'previous', capfirst(_("previous"))),
            self.arrow(next, 'next', capfirst(_("next"))),
            self.arrow(last, 'last', capfirst(_("last"))),
            ))

    def navigation(self, title, min_count=2, already=0, **kwargs):
        total = Screenshot.objects.filter(**kwargs).count()
        if total < min_count or total == already:
            return ''
        index = Screenshot.objects.filter(id__lt=self.id, **kwargs).count() + 1
        index = _("%(index)d out of %(total)d") % locals()
        arrows = self.arrows(**kwargs)
        return '\n'.join((
            '<tr>',
            '<th>%s:</th>' % title,
            '<td class="index">%s</span>' % index,
            '<td class="arrows">%s</td>' % arrows,
            '</tr>',
            ))

    def website_navigation(self):
        """
        Navigation links to other screenshots of the same website.
        """
        return self.navigation(
            capfirst(_("screenshot")),
            min_count=1,
            website=self.website)

    def browser_navigation(self):
        """
        Navigation links for screenshots of the same browser.
        """
        return self.navigation(
            self.browser.browser_group.name,
            already=Screenshot.objects.filter(website=self.website).count(),
            website=self.website,
            browser__browser_group=self.browser.browser_group)

    def platform_navigation(self):
        platform = self.factory.operating_system.platform
        return self.navigation(
            platform.name,
            already=Screenshot.objects.filter(website=self.website).count(),
            website=self.website,
            factory__operating_system__platform=platform)
