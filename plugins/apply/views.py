from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django import newforms as forms
from shotserver04.apply.models import Candidate

CandidateForm = forms.form_for_model(Candidate)


@login_required
def apply(http_request):
    """
    Partner application form.
    """
    form_title = "Want to join Browsershots?"
    form_action = '/apply/'
    form = CandidateForm(http_request.POST or None)
    form_submit = "submit"
    form_extra_before = '<p class="admonition warning">%s<p>' % ' '.join((
            "This page is only a mock-up.",
            "Your info will not be saved.",
            "Please try again later.",
            ))
    form_extra = '<ul>\n%s\n</ul>' % '\n'.join(
        map(lambda text: '<li>%s</li>' % text, (
"All fields are optional.",
"To edit your information later, simply come back to this page.",
'<a href="http://trac.browsershots.org/wiki/BlogStartupFoundersWanted">' +
"More information is available in the wiki." +
'</a>')))
    return render_to_response('form.html', locals(),
        context_instance=RequestContext(http_request))
