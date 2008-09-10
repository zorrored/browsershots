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
Django admin for browsers app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.contrib import admin
from shotserver05.browsers.models import BrowserName, Engine, Browser


class BrowserNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}
    ordering = ('slug', )


class EngineAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}
    ordering = ('slug', )


class BrowserAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'engine', 'engine_version', 'factory')
    ordering = ('name', 'version', 'factory')


admin.site.register(BrowserName, BrowserNameAdmin)
admin.site.register(Engine, EngineAdmin)
admin.site.register(Browser, BrowserAdmin)
