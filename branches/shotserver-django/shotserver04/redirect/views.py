from xmlrpclib import Fault
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from shotserver04.nonces import xmlrpc as nonces
from shotserver04.factories.models import Factory
from shotserver04.requests.models import Request
from shotserver04.browsers.models import Browser
from datetime import datetime


def redirect(http_request, factory_name, encrypted_password, request_id):
    try:
        factory = get_object_or_404(Factory, name=factory_name)
        status = nonces.verify(http_request, factory, encrypted_password)
        if status != 'OK':
            raise Fault(0, status)
        request = get_object_or_404(Request, id=request_id)
        request.check_factory_lock(factory)
        user_agent = http_request.META['HTTP_USER_AGENT']
        try:
            browser = Browser.objects.get(
                factory=factory, user_agent=user_agent)
        except Browser.DoesNotExist:
            raise Fault(0, "Unknown user agent: %s." % user_agent)
        request.browser = browser
        request.redirected = datetime.now()
        request.save()
        website = request.request_group.website
        return HttpResponseRedirect(website.url)
    except Fault, fault:
        return render_to_response('redirect/error.html',
                                  {'message': fault.faultString})
