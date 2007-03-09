from django.shortcuts import render_to_response
from django.http import Http404
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser

FACTORY_LIST_COLUMNS = (
    'name',
    'operating_system',
    'architecture',
    'last_poll',
    'last_upload',
    'uploads_per_hour',
    'uploads_per_day',
)


def factory_list(request):
    order = request.GET.get('order', '')
    order_column = order
    descending = order.startswith('-')
    if descending:
        order_column = order[1:]
    if order_column not in FACTORY_LIST_COLUMNS:
        order = order_column = 'name'
        descending = False
    header_list = []
    for column in FACTORY_LIST_COLUMNS:
        text = column.replace('_', ' ').replace(' ', '<br />', 1)
        class_attrib = ''
        if column == order_column:
            found = True
            if descending:
                class_attrib = ' class="sorted descending"'
                url = '?order=' + column
            else:
                class_attrib = ' class="sorted ascending"'
                url = '?order=-' + column
        else:
            url = '?order=' + column
        header_list.append({'text': text,
                            'url': url,
                            'class_attrib': class_attrib})
    factory_list = list(Factory.objects.order_by(order))
    return render_to_response('factories/factory_list.html', locals())


def factory_detail(request, factory_name):
    try:
        factory = Factory.objects.get(name=factory_name)
    except Factory.DoesNotExist:
        raise Http404
    browser_list = Browser.objects.filter(factory=factory.id)
    screensize_list = factory.screensize_set.all()
    colordepth_list = factory.colordepth_set.all()
    return render_to_response('factories/factory_detail.html', locals())
