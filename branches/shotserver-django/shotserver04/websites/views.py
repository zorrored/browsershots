from django.db import connection
from django.http import Http404
from django.shortcuts import render_to_response
from shotserver04.websites.models import Website


def website_list(request):
    website_list = Website.objects
    search_query = request.GET.get('q', '')
    for search in search_query.split():
        if search.islower(): # Case insensitive search
            website_list = website_list.filter(url__icontains=search)
        else: # Case sensitive search if mixed case in query
            website_list = website_list.filter(url__contains=search)
    website_list = website_list.order_by('-submitted')
    website_list = website_list[:100]
    query_list = connection.queries
    return render_to_response('websites/website_list.html', locals())


def website_detail(request, website_url):
    try:
        website = Website.objects.get(url=website_url)
    except Website.DoesNotExist:
        website = None
    query_list = connection.queries
    return render_to_response('websites/website_detail.html', locals())
