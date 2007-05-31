from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from shotserver04.nonces import xmlrpc as nonces
from shotserver04.factories.models import Factory
from shotserver04.requests.models import Request


def redirect(request, factory_name, encrypted_password, request_id):
    factory = get_object_or_404(Factory, name=factory_name)
    status = nonces.verify(request, factory, encrypted_password)
    if status != 'OK':
        render_to_response('redirect/error.html', locals())
    request = get_object_or_404(Request, id=request_id)
    website = request.request_group.website
    return HttpResponseRedirect(website.url)
