from django.shortcuts import render_to_response
from shotserver04.websites.models import Website


def website_detail(request, website_url):
    try:
        website = Website.objects.get(url=website_url)
    except Website.DoesNotExist:
        website = None
    return render_to_response('websites/website_detail.html', locals())
