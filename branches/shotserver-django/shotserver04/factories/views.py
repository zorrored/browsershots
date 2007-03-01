from django.shortcuts import render_to_response
from shotserver04.factories.models import Factory


def index(request):
    factory_list = Factory.objects.all()
    return render_to_response('factories/index.html',
                              {'factory_list': factory_list})
