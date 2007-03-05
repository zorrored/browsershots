from django.shortcuts import render_to_response
from django.http import Http404
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser


def factory_detail(request, factory_name):
    try:
        factory = Factory.objects.get(name=factory_name)
    except Factory.DoesNotExist:
        raise Http404
    browser_list = Browser.objects.filter(factory=factory.id)
    return render_to_response('factories/factory_detail.html', locals())
