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
Screenshot views.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import cgi
import zipfile
import tempfile
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django import newforms as forms
from django.utils.translation import ugettext_lazy as _
from django.core.servers.basehttp import FileWrapper
from shotserver04.common.preload import preload_foreign_keys
from shotserver04.screenshots.models import Screenshot, ProblemReport
from shotserver04.screenshots import storage
from shotserver04.requests.models import Request, RequestGroup
from shotserver04 import settings

COLUMNS = 10
WIDTH = 80 # pixels
MARGIN = 12 # pixels

PROBLEM_CHOICES = [
    (101, _("This is not %(browser)s.")),
    (102, _("This is not %(operating_system)s.")),

    (201, _("Javascript is not %(javascript)s.")),
    (202, _("Java is not %(java)s.")),
    (203, _("Flash is not %(flash)s.")),
    (204, _("A language pack needs to be installed.")),

    (601, _("There is a dialog box in front of the browser window.")),
    (602, _("The browser window is not maximized.")),
    (603, _("The page is not finished loading.")),

    (999, ''),
    ]


def overview(http_request):
    """
    Full-screen display of recent screenshots (one per website).
    """
    columns = [[0, index * (WIDTH + MARGIN)] for index in range(COLUMNS)]
    previews = []
    screenshots = list(Screenshot.objects.recent())
    preload_foreign_keys(screenshots, website=True)
    for screenshot in screenshots:
        if screenshot.website.profanities > settings.PROFANITIES_ALLOWED:
            continue
        width = WIDTH
        height = screenshot.height * width / screenshot.width
        columns.sort()
        top, left = columns[0]
        previews.append(
            screenshot.preview_div(
            style=u"left:%dpx;top:%dpx;position:absolute" % (left, top),
            title=screenshot.website.url,
            href=screenshot.website.get_absolute_url()))
        columns[0][0] += height + MARGIN
    columns.sort()
    previews.insert(0,
        u'<div class="previews" style="height:%dpx">' % columns[-1][0])
    previews.append('</div>')
    previews = '\n'.join(previews)
    return render_to_response('screenshots/overview.html', locals())


class ProblemForm(forms.Form):
    code = forms.ChoiceField(widget=forms.RadioSelect)
    message = forms.CharField(max_length=200, required=False)

    def clean_message(self):
        message = self.cleaned_data['message'].lower()
        if '<' in message and '>' in message:
            raise forms.ValidationError(
                unicode(_("HTML is not allowed here.")))
        for word in 'http:// https:// www. .com .net .org'.split():
            if word in message:
                raise forms.ValidationError(
                    unicode(_("URLs are not allowed here.")))
        return cgi.escape(self.cleaned_data['message'])


def details(http_request, hashkey):
    """
    Show large preview and detailed information about a screenshot.
    """
    screenshot = get_object_or_404(Screenshot, hashkey=hashkey)
    request = Request.objects.get(screenshot=screenshot)
    problem_form = ProblemForm(http_request.POST)
    requested = {
        'browser': unicode(screenshot.browser),
        'operating_system': unicode(screenshot.factory.operating_system),
        'java': unicode(screenshot.browser.java),
        'javascript': unicode(screenshot.browser.javascript),
        'flash': unicode(screenshot.browser.flash),
        }
    problem_form.fields['code'].choices = [
        (code, message % requested) for code, message in PROBLEM_CHOICES]
    if problem_form.is_valid():
        if int(problem_form.cleaned_data['code']) != 999:
            for code, message in PROBLEM_CHOICES:
                if int(problem_form.cleaned_data['code']) == code:
                    problem_form.cleaned_data['message'] = message % requested
        if problem_form.cleaned_data['message']:
            ProblemReport.objects.create(
                screenshot=screenshot,
                ip=http_request.META['REMOTE_ADDR'],
                **problem_form.cleaned_data)
            return HttpResponseRedirect(
                request.factory.get_absolute_url() + '#problems')
    select_message = "document.problem_form.code[%d].checked=true" % (
        len(PROBLEM_CHOICES) - 1)
    message_field = problem_form['message'].as_text(
        {'onclick': select_message,
         'onchange': 'if (this.value) ' + select_message})
    return render_to_response('screenshots/details.html', locals())


def download_zip(http_request, request_group_id):
    """
    Output a ZIP file containing all screenshots in a request group.
    """
    request_group = get_object_or_404(RequestGroup, id=request_group_id)
    requests = request_group.request_set.filter(screenshot__isnull=False)
    preload_foreign_keys(requests, screenshot=True)
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_STORED)
    for request in requests:
        filename = storage.png_filename(request.screenshot.hashkey)
        archive.write(filename, str(request.screenshot.png_filename()))
    archive.close()
    # Send result to browser
    response = HttpResponse(FileWrapper(temp), content_type='application/zip')
    response['Content-Disposition'] = 'attachment' # ; filename=screenshots.zip
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response
