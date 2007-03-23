from django.shortcuts import render_to_response
from django import newforms as forms
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser


class URLForm(forms.Form):
    url = forms.URLField(max_length=400)


class OptionsForm(forms.Form):
    maximum_wait = forms.ChoiceField(initial=30, choices=(
        (15, "15 minutes"),
        (30, "30 minutes"),
        (60, "1 hour"),
        (120, "2 hours"),
        (240, "4 hours"),
        ))
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


class BrowserForm(forms.BaseForm):

    def __init__(self, data=None):
        forms.BaseForm.__init__(self)
        self.data = data
        for factory in Factory.objects.filter(uploads_per_hour__gt=0):
            self.fields[factory.name] = forms.BooleanField()

    errors = {}
    base_fields = forms.forms.SortedDictFromList()

    #def __unicode__(self):
    #    return u'\n'.join(self.fields)


def start(request):
    if request.POST:
        url_form = URLForm(request.POST)
        options_form = OptionsForm(request.POST)
        browser_form = BrowserForm(request.POST)
    else:
        url_form = URLForm()
        options_form = OptionsForm()
        browser_form = BrowserForm()
    return render_to_response('start.html', locals())
