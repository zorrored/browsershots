from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from shotserver04.factories.models import Factory


@login_required
def profile(http_request):
    factory_table_header = Factory.table_header()
    factory_list = Factory.objects.filter(admin=http_request.user)
    return render_to_response('accounts/profile.html', locals())
