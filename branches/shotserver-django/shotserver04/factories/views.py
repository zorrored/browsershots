from django.shortcuts import render_to_response
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser


def index(request):
    factory_list = Factory.objects.all()
    return render_to_response('factories/index.html',
                              {'factory_list': factory_list})


def details(request, factory_name):
    factory = Factory.objects.get(name=factory_name)
    return render_to_response(
        'factories/details.html',
        {'factory_name': factory_name,
         'browser_list': Browser.objects.filter(factory=factory.id)})
