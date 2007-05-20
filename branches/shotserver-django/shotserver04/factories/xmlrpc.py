from shotserver04.factories.models import Factory
from shotserver04.requests.models import Request


def features(request, factory_name):
    """
    factories.features('factory') => '(screensize = 640)'
    """
    factory = Factory.objects.get(name=factory_name)
    joins, where, params = factory.features_q().get_sql(Request._meta)
    where = ' AND '.join(where)
    for index in range(len(params)):
        if params[index] is None:
            params[index] = 'NULL'
    return where % tuple(params)
