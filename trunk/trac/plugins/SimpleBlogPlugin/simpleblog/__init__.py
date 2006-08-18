from trac.core import *
from trac.web import IRequestHandler
from trac.web.chrome import add_link, INavigationContributor, ITemplateProvider
from trac.wiki.api import WikiSystem
from trac.wiki.model import WikiPage
from trac.wiki.formatter import wiki_to_html
from trac.util import Markup, format_date, format_datetime, http_date
from pkg_resources import resource_filename

import re
title_split_match = re.compile(r'^=+\s+(\S.*\S)\s+=+\s+(.*)$').match

class SimpleBlogPlugin(Component):
    implements(INavigationContributor, ITemplateProvider, IRequestHandler)

    # INavigationContributor methods
    def get_active_navigation_item(self, req):
        return 'blog'
    def get_navigation_items(self, req):
        yield 'mainnav', 'blog', Markup(
            '<a href="%s">Blog</a>' % self.env.href.blog())

    # ITemplateProvider methods
    def get_templates_dirs(self):
        return [resource_filename(__name__, 'templates')]
    def get_htdocs_dirs(self):
        return []

    # IRequestHandler methods
    def match_request(self, req):
        return req.path_info == '/blog'
    def process_request(self, req):
        req.hdf['trac.href.blog'] = req.href.blog()

        entries = []
        for page_name in WikiSystem(self.env).get_pages(prefix='Blog'):
            page = WikiPage(self.env, page_name)
            title = page
            text = page.text

            match = title_split_match(page.text)
            if match:
                title = match.group(1)
                text = match.group(2)

            description = wiki_to_html(text, self.env, req)

            event = {
                'href': self.env.href.wiki(page_name),
                'title': title,
                'description': description,
                'escaped': Markup.escape(str(description)),
                'author': page.author,
                'date': format_datetime(page.time),
                'rfcdate': http_date(page.time),
                }
            entries.append((page.time, event))
        entries.sort()
        entries.reverse()
        events = []
        for date, event in entries:
            events.append(event)
        req.hdf['blog.events'] = events

        format = req.args.get('format')
        if format == 'rss':
            return 'blog_rss.cs', 'application/rss+xml'

        add_link(req, 'alternate', self.env.href.blog(format='rss'),
                 'RSS Feed', 'application/rss+xml', 'rss')
        return 'blog.cs', None
