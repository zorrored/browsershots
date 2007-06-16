from django.conf import settings
from django import http


class RedirectMiddleware(object):
    """
    Append missing slashes, but if path starts with the name of an
    installed app. Special URLs will be left untouched.

    Also redirect to XML-RPC documentation if subdomain is 'api' or
    'xmlrpc' and path is '/'.
    """

    def process_request(self, request):
        # Don't rewrite POST requests
        if not request.method in ('GET', 'HEAD'):
            return
        first_part = request.path.strip('/').split('/')[0]
        # Redirect to XML-RPC documentation
        host = http.get_host(request)
        subdomain = host.lower().split('.')[0]
        if subdomain in ('api', 'xmlrpc') and first_part == '':
            return http.HttpResponsePermanentRedirect('/xmlrpc/')
        # Add trailing slash if path starts with an installed app name
        if self.installed_app(first_part) and not request.path.endswith('/'):
            new_path = request.path + '/'
            if request.GET:
                new_path += '?' + request.GET.urlencode()
            return http.HttpResponsePermanentRedirect(new_path)

    def installed_app(self, name):
        """
        Check if this is the name of an installed app.
        """
        name = '.' + name
        for app in settings.INSTALLED_APPS:
            if app.endswith(name):
                return True
