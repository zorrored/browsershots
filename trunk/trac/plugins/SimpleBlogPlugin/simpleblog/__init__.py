from trac.core import *
from trac.web import IRequestHandler
from trac.web.chrome import INavigationContributor
from trac.wiki.api import WikiSystem
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
    def match_request(self, req):
        return req.path_info == '/blog'
    def process_request(self, req):
        req.hdf['wiki.action'] = 'view'
        page_html = []
        for page in WikiSystem(self.env).get_pages():
            page_html.append(repr(page))
        req.hdf['wiki.page_html'] = '\n'.join(page_html)
        return 'wiki.cs', None
