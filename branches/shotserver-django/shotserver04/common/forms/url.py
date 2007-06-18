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
URL input form.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django import newforms as forms
from shotserver04.websites import extract_domain
from shotserver04.websites.models import Domain, Website


class UrlForm(forms.Form):
    """
    URL input form.
    """
    url = forms.URLField(
        max_length=400,
        label=_("Enter your web address here:"))

    def cleaned_dict(self):
        """
        Get or create domain and website.
        """
        url = self.cleaned_data['url']
        if url.count('/') == 2:
            url += '/' # Slash after domain name
        domain, created = Domain.objects.get_or_create(
            name=extract_domain(url, remove_www=True))
        website, created = Website.objects.get_or_create(
            url=url, domain=domain)
        return {'website': website}
