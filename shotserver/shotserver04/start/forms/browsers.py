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
Automatic form with active browsers for each platform.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django import newforms as forms

try:
    all([])
except NameError:
    def all(sequence):
        for element in sequence:
            if not bool(element):
                return False
        return True


class BrowsersForm(forms.BaseForm):
    """
    Browser chooser form for one platform.
    """

    errors = {}
    base_fields = forms.forms.SortedDictFromList()

    def __init__(self, active_browsers, platform, data=None):
        forms.BaseForm.__init__(self, data)
        self.platform = platform
        self.columns = 1
        field_dict = {}
        for browser in active_browsers:
            if browser.factory.operating_system.platform_id != platform.id:
                continue
            label = browser.browser_group.name
            if browser.major is not None:
                label += ' ' + str(browser.major)
                if browser.minor is not None:
                    label += '.' + str(browser.minor)
            name = '_'.join((
                platform.name.lower().replace(' ', '-'),
                browser.browser_group.name.lower().replace(' ', '-'),
                str(browser.major),
                str(browser.minor),
                ))
            if name in field_dict:
                continue
            if data:
                initial = name in data and 'on' in data[name]
            else:
                initial = all([
                    other.minor <= browser.minor
                    for other in active_browsers
                    if other.browser_group == browser.browser_group
                    and other.major == browser.major])
            field = forms.BooleanField(
                label=label, initial=initial, required=False)
            field_dict[name] = field
        field_names = field_dict.keys()
        field_names.sort()
        for name in field_names:
            self.fields[name] = field_dict[name]

    def __unicode__(self):
        fields = list(self.fields)
        output = []
        for column in range(self.columns):
            output.append('<div class="browsers_column">')
            for index in range(self.column_length()):
                if not fields:
                    break
                field = fields.pop(0)
                output.append(unicode(self[field]) +
                    u' <label for="id_%s">%s</label><br />' % (
                    field, self[field].label))
            output.append('</div>')
        return u'\n'.join(output)

    def column_length(self):
        """Get the length of the longest column after wrapping."""
        return (len(self.fields) + self.columns - 1) / self.columns
