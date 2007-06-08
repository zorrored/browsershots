from django.shortcuts import render_to_response, get_object_or_404
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
    return render_to_response('websites/website_list.html', locals())


def website_detail(request, website_url):
    website = get_object_or_404(Website, url=website_url)
    return render_to_response('websites/website_detail.html', locals())


def website_numeric(request, website_id):
    website = get_object_or_404(Website, id=website_id)
    return render_to_response('websites/website_detail.html', locals())
