from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from shotserver04.requests.models import Request


def request_list(http_request):
    request_list = Request.objects.select_related().order_by(
        '-requests_requestgroup.submitted')[:100]
    return render_to_response('requests/request_list.html', locals())
