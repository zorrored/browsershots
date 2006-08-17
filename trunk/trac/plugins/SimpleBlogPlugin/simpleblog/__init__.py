from trac.core import *
from trac.web import IRequestHandler
from trac.web.chrome import INavigationContributor
from trac.wiki.api import WikiSystem
from trac.wiki.model import WikiPage
from trac.wiki.formatter import wiki_to_html
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
        entries = []
        for page_name in WikiSystem(self.env).get_pages(prefix='Blog'):
            page = WikiPage(self.env, page_name)
            html = wiki_to_html(page.text, self.env, req)
            entries.append((page.time, html))
        entries.sort()
        entries.reverse()
        page_html = []
        for date, html in entries:
            page_html.append(html)
            human_time = format_datetime(date)
            page_html.append('<p>%s</p>' % human_time)
        req.hdf['wiki.page_html'] = Markup('\n'.join(page_html))
        return 'wiki.cs', None
