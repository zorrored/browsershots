from django import newforms as forms
from shotserver04.factories.models import ScreenSize, ColorDepth
from shotserver04.common import last_poll_timeout, int_or_none
from shotserver04.common import lazy_gettext_capfirst as _
from datetime import datetime, timedelta


def screen_size_choices():
    yield ('dontcare', _("don't care"))
    for size in ScreenSize.objects.filter(
        factory__last_poll__gt=last_poll_timeout()):
        yield (size.width, str(size))


def color_depth_choices():
    yield ('dontcare', _("don't care"))
    for depth in ColorDepth.objects.filter(
        factory__last_poll__gt=last_poll_timeout()):
        yield (depth.bits_per_pixel, str(depth))


class OptionsForm(forms.Form):
    """
    Request options input form.
    """
    screen_size = forms.ChoiceField(
        label=_("screen size"),
        initial='dontcare',
        choices=screen_size_choices())
    color_depth = forms.ChoiceField(
        label=_("color depth"),
        initial='dontcare',
        choices=color_depth_choices())
    maximum_wait = forms.ChoiceField(
        label=_("maximum wait"),
        initial=30, choices=(
        (15, _("15 minutes")),
        (30, _("30 minutes")),
        (60, _("1 hour")),
        (120, _("2 hours")),
        (240, _("4 hours")),
        ))

    def cleaned_dict(self):
        """
        Convert options to integer and timestamp.
        """
        return {
            'expire': datetime.now() + timedelta(
                minutes=int(self.cleaned_data['maximum_wait'])),
            'width': int_or_none(self.cleaned_data['screen_size']),
            'bits_per_pixel': int_or_none(self.cleaned_data['color_depth']),
            }
