from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from shotserver05.factories.models import Factory
from shotserver05.factories.forms import FactoryForm


def index(request):
    return render_to_response('factories/index.html', locals(),
                              context_instance=RequestContext(request))


def details(request, name):
    factory = get_object_or_404(Factory, name=name)
    form = FactoryForm(instance=factory)
    return render_to_response('factories/details.html', locals(),
                              context_instance=RequestContext(request))
