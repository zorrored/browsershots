from django.shortcuts import render_to_response


def profile(http_request):
    return render_to_response('accounts/profile.html', locals())
