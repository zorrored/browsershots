from trac.core import *
from trac.web import IRequestHandler
from trac.web.chrome import INavigationContributor
from trac.util import Markup, format_date, format_datetime

class SimpleBlogPlugin(Component):
    implements(INavigationContributor, IRequestHandler)

    # INavigationContributor methods
    def get_active_navigation_item(self, req):
        return 'blog'
    def get_navigation_items(self, req):
        yield 'mainnav', 'blog', Markup(
            '<a href="%s">Blog</a>' % self.env.href.blog())

    # IRequestHandler methods
    anonymous_request = True
    use_template = False
    def match_request(self, req):
        return req.path_info == '/blog'
    def process_request(self, req):
        req.send_response(200)
        req.send_header('Content-Type', 'text/plain')
        req.end_headers()
        req.write('Mein Blog!')
