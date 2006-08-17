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
    def match_request(self, req):
        return req.path_info == '/blog'
    def process_request(self, req):
        req.hdf['wiki.action'] = 'view'
        req.hdf['wiki.page_html'] = 'Hallo Welt!'
        return 'wiki.cs', None
