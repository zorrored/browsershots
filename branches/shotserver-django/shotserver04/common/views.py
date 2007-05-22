from django.db import connection
from django.http import HttpResponseRedirect
from django import newforms as forms
from django.shortcuts import render_to_response
from shotserver04.factories.models import OperatingSystemGroup, Factory
from shotserver04.browsers.models import BrowserGroup, Browser
from shotserver04.websites.models import Website
from shotserver04.requests.models import RequestGroup, Request
from datetime import datetime, timedelta


class URLForm(forms.Form):
    url = forms.URLField(max_length=400)


class OptionsForm(forms.Form):
    screen_size = forms.ChoiceField(initial='any', choices=(
        ('any', "Don't Care"),
        (640, "640x480"),
        (800, "800x600"),
        (1024, "1024x768"),
        (1280, "1280x1024"),
        (1600, "1600x1200"),
        ))
    color_depth = forms.ChoiceField(initial='any', choices=(
        ('any', "Don't Care"),
        (4, "4 Bits (16 Colors)"),
        (8, "8 Bits (256 Colors)"),
        (16, "16 Bits (High Color)"),
        (24, "24 Bits (True Color)"),
        ))
    javascript = forms.ChoiceField(initial='any', choices=(
        ('any', "Don't Care"),
        ('no', "Disabled"),
        ('yes', "Enabled"),
        ))
    java = forms.ChoiceField(initial='any', choices=(
        ('any', "Don't Care"),
        ('no', "Disabled"),
        ('yes', "Enabled"),
        ))
    flash = forms.ChoiceField(initial='any', choices=(
        ('any', "Don't Care"),
        ('no', "Disabled"),
        ('yes', "Enabled"),
        (5, "Version 5"),
        (6, "Version 6"),
        (7, "Version 7"),
        (8, "Version 8"),
        (9, "Version 9"),
        ))
    maximum_wait = forms.ChoiceField(initial=30, choices=(
        (15, "15 minutes"),
        (30, "30 minutes"),
        (60, "1 hour"),
        (120, "2 hours"),
        (240, "4 hours"),
        ))


class BrowserForm(forms.BaseForm):

    errors = {}
    base_fields = forms.forms.SortedDictFromList()

    def __init__(self, os, data=None):
        forms.BaseForm.__init__(self, data)
        self.parts = 1
        browsers = Browser.objects.select_related()
        os_browsers = browsers.filter(
            factory__operating_system__operating_system_group__name=os,
            disabled=False)
        active_browsers = os_browsers.extra(
            where=['"factories_factory"."last_poll" > NOW() - %s::interval'],
            params=['31d'])
        field_dict = {}
        for browser in active_browsers:
            label = browser.browser_group.name
            if browser.major is not None:
                label += ' ' + str(browser.major)
                if browser.minor is not None:
                    label += '.' + str(browser.minor)
            name = (os + ' ' + label).lower()
            name = name.replace(' ', '_').replace('.', '_')
            if name in field_dict:
                continue
            initial = data is None or (name in data and 'on' in data[name])
            field = forms.BooleanField(label=label, initial=initial)
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


def start(request):
    post = request.POST or None
    url_form = URLForm(post)
    options_form = OptionsForm(post)
    linux_browsers = BrowserForm('Linux', post)
    windows_browsers = BrowserForm('Windows', post)
    mac_browsers = BrowserForm('Mac OS', post)
    # Validate all forms
    valid_post = (url_form.is_valid() and options_form.is_valid() and
        linux_browsers.is_valid() and windows_browsers.is_valid() and
        mac_browsers.is_valid())
    if valid_post:
        # Submit URL
        url=url_form.cleaned_data['url']
        if url.count('/') == 2:
            url += '/' # Trailing slash
        website, created = Website.objects.get_or_create(url=url)
        # Calculate expiration timeout
        minutes = int(options_form.cleaned_data['maximum_wait'])
        timeout = timedelta(0, minutes * 60, 0)
        expire = datetime.now() + timeout
        # Submit request group
        request_group = RequestGroup.objects.create(
            website=website,
            width=try_int(options_form.cleaned_data['screen_size']),
            bits_per_pixel=try_int(options_form.cleaned_data['color_depth']),
            javascript=options_form.cleaned_data['javascript'],
            java=options_form.cleaned_data['java'],
            flash=options_form.cleaned_data['flash'],
            expire=expire,
            )
        request_list = (
            create_os_requests(request_group, 'Linux', linux_browsers) +
            create_os_requests(request_group, 'Windows', windows_browsers) +
            create_os_requests(request_group, 'Mac OS', mac_browsers)
            )
        return render_to_response('debug.html', locals())
        return HttpResponseRedirect('/' + url_form.cleaned_data['url'])
    else:
        # Show HTML form
        linux_browsers.parts = 2
        query_list = connection.queries
        return render_to_response('start.html', locals())


def create_os_requests(request_group, os_name, browser_form):
    os_groups = OperatingSystemGroup.objects.filter(name=os_name)
    if not len(os_groups):
        return []
    os_group = os_groups[0]
    result = []
    for name in browser_form.fields:
        os_name, browser_name, major, minor = name.split('_')
        assert os_group.name.lower().startswith(os_name)
        browser_group = BrowserGroup.objects.get(name__iexact=browser_name)
        result.append(Request.objects.create(
            request_group=request_group,
            operating_system_group=os_group,
            browser_group=browser_group,
            major=try_int(major),
            minor=try_int(minor),
            ))
    return result


def try_int(value):
    if value.isdigit():
        return int(value)
