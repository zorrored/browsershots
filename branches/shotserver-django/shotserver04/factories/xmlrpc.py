from shotserver04.factories.models import Factory


def features(request, factory_name):
    """
    factories.features('factory') => '(screensize = 640)'
    """
    factory = Factory.objects.get(name=factory_name)
    return factory.features_sql()
