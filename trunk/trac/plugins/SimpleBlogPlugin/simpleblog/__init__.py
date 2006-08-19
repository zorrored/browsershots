from trac.core import *
from trac.web import IRequestHandler
from trac.web.chrome import add_link, INavigationContributor, ITemplateProvider
from trac.wiki.api import WikiSystem, IWikiMacroProvider
from trac.wiki.model import WikiPage
from trac.wiki.formatter import wiki_to_html
from trac.util import Markup, format_date, format_datetime, http_date
from pkg_resources import resource_filename

import re
# title_split_match = re.compile(r'^=+\s+(\S.*\S)\s+=+\s+(.*)$').match
title_split_match = re.compile(r'^=+\s+([^\n\r=]+?)\s+=+\s+(.+)$', re.DOTALL).match

from md5 import md5

class SimpleBlogPlugin(Component):
    implements(INavigationContributor, ITemplateProvider,
               IWikiMacroProvider, IRequestHandler)

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

    # IWikiMacroProvider methods
    def get_macros(self):
        yield 'SimpleBlogComment'
    def get_macro_description(self, name):
        if name == 'SimpleBlogComment':
            return 'Format the header of a blog comment for HTML output.'
    def render_macro(self, req, name, content):
        if name == 'SimpleBlogComment':
            return self._simple_blog_comment(req, content)

    def _simple_blog_comment(self, req, content):
        comment = {}
        for key in 'author email ip posted title website'.split():
            pos = content.find(key + '="')
            if pos >= 0:
                start = pos + len(key) + 2
                stop = content.index('"', start)
                value = content[start:stop].strip()
                if value:
                    comment[key] = value
        if not comment.has_key('title'):
            comment['title'] = 'Comment'
        output = ['</p>']
        output.append('<p style="clear: both;"></p>')
        if comment.has_key('email'):
            output.append('<div style="float: left; margin: 0 1em 2px -18px; border-bottom-style: none;">' +
                          '<a href="http://www.gravatar.com/">' +
                          '<img src="http://www.gravatar.com/avatar.php?gravatar_id=' + md5(comment['email']).hexdigest() +
                          '&amp;rating=R&amp;size=40&amp;default=http%3A%2F%2Fv03.browsershots.org%2Fstyle%2Fgravatar40.png"' +
                          ' alt="Gravatar" width="40" height="40" style="vertical-align: middle;" /></a></div>')
            output.append('<h2 style="float: left; margin: 0 1ex 0 0;">%(title)s</h2>' % comment)
        else:
            output.append('<h2 style="float: left; margin: 0 1ex 0 -18px;">%(title)s</h2>' % comment)
        output.append('<p style="font-size: smaller; color: gray; padding-top: 2px;">')
        if comment.has_key('posted'):
            output.append('posted %(posted)s' % comment)
        if comment.has_key('author'):
            if comment.has_key('website'):
                output.append('by <a href="%(website)s" class="ext-link"><span class="icon">%(author)s</span></a>' % comment)
            else:
                output.append('by %(author)s' % comment)
        return Markup('\n'.join(output))

    # IRequestHandler methods
    def match_request(self, req):
        return req.path_info == '/blog'
    def process_request(self, req):
        req.hdf['trac.href.blog'] = req.href.blog()

        entries = []
        for page_name in WikiSystem(self.env).get_pages(prefix='Blog'):
            page = WikiPage(self.env, page_name)
            title = page_name
            text = page.text

            match = title_split_match(page.text)
            if match:
                title = match.group(1)
                text = match.group(2)

            comments = text.count('[[SimpleBlogComment(')
            cutoff = text.find('[[SimpleBlogComment(')
            if cutoff >= 0:
                text = text[:cutoff].rstrip()
            description = wiki_to_html(text, self.env, req)

            original = self._get_original_post_info(page_name)
            event = {
                'href': self.env.href.wiki(page_name),
                'title': title,
                'description': description,
                'escaped': Markup.escape(unicode(description)),
                'date': format_datetime(original.time),
                'rfcdate': http_date(original.time),
                'author': original.author,
                'comment': original.comment,
                'comments': comments,
                }
            if page.version > 1:
                event['updated.version'] = page.version
                event['updated.date'] = format_datetime(page.time)
                event['updated.rfcdate'] = http_date(page.time)
                event['updated.author'] = page.author
                event['updated.comment'] = page.comment
            entries.append((original.time, event))

        entries.sort()
        entries.reverse()
        max_count = 20
        if len(entries) > max_count:
            entries = entries[:max_count]

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

    def _get_original_post_info(self, page_name):
        db = self.env.get_db_cnx()
        cursor = db.cursor()
        cursor.execute("SELECT time,author,comment,ipnr FROM wiki "
                       "WHERE name=%s AND version=1", (page_name, ))
        return cursor.fetchone()
