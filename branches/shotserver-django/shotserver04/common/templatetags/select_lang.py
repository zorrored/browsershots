from django import template
from django.db import connection
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
