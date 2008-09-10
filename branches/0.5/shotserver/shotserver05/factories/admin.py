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
Django admin for factories app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.contrib import admin
from shotserver05.factories.models import Factory, ScreenSize, ColorDepth
from shotserver05.browsers.models import Browser


class ScreenSizeInline(admin.TabularInline):
    model = ScreenSize
    extra = 1


class ColorDepthInline(admin.TabularInline):
    model = ColorDepth
    extra = 1


class BrowserInline(admin.TabularInline):
    model = Browser
    extra = 1


class FactoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    ordering = ('name', )
    inlines = (ScreenSizeInline, ColorDepthInline, BrowserInline)


admin.site.register(Factory, FactoryAdmin)
admin.site.register(ScreenSize)
admin.site.register(ColorDepth)
