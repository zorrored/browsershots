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
Show language selector.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django import template
from django.conf import settings
from django.utils import translation

register = template.Library()

JAVASCRIPT = ''.join("""
document.location.href='/i18n/setlang/?language='+
this.form.language.options[this.form.language.options.selectedIndex].value;
""".splitlines()).strip()

FORM_TEMPLATE = """
<form action="/i18n/setlang/" method="get">
<div id="setlang">
<select name="language" id="language" onchange="%s">
%s
</select>
</div>
</form>
""".strip()


@register.simple_tag
def select_lang():
    options = []
    current = translation.get_language()
    for lang, name in settings.LANGUAGES:
        sel = ''
        if lang == current:
            sel = ' selected="selected"'
        options.append('<option value="%s"%s>%s</option>' % (lang, sel, name))
    return FORM_TEMPLATE % (JAVASCRIPT, '\n'.join(options))
