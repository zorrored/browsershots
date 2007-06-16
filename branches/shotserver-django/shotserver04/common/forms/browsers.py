from django import newforms as forms
from shotserver04.browsers.models import BrowserGroup, Browser
from shotserver04.common import last_poll_timeout


class BrowsersForm(forms.BaseForm):
    """
    Browser chooser form for one platform.
    """

    errors = {}
    base_fields = forms.forms.SortedDictFromList()

    def __init__(self, platform, data=None):
        forms.BaseForm.__init__(self, data)
        self.platform = platform
        self.parts = 1
        active_browsers = Browser.objects.filter(
            factory__operating_system__platform=platform,
            factory__last_poll__gt=last_poll_timeout(),
            active=True)
        field_dict = {}
        for browser in active_browsers:
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
            initial = data is None or (name in data and 'on' in data[name])
            field = forms.BooleanField(
                label=label, initial=initial, required=False)
            field_dict[name] = field
        field_names = field_dict.keys()
        field_names.sort()
        for name in field_names:
            self.fields[name] = field_dict[name]

    def __unicode__(self):
        fields = list(self.fields)
        fields_per_part = (len(fields) + self.parts - 1) / self.parts
        output = []
        for part in range(self.parts):
            output.append('<div style="width:12em;float:left">')
            for index in range(fields_per_part):
                if not fields:
                    break
                field = fields.pop(0)
                output.append(unicode(self[field]) +
                    ' <label for="id_%s">%s</label><br />' % (
                    field, self[field].label))
            output.append('</div>')
        return u'\n'.join(output)
