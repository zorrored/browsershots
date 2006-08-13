# vim: tabstop=4 shiftwidth=4 expandtab
"""
Creates Yahoo style navigation

Revisions:
    1.1 (20041205) - Steven Armstrong - changed to work with category and calendar url's,
        changed so that /static and 404 requests are not handled
    1.0 ? - Wari Wahab

$Id: breadcrumbs.py,v 1.2 2006/03/22 20:53:52 sar Exp $
"""
__author__ = "Wari Wahab - wari at wari dot per dot sg"
__version__ = "1.1 (20041204)"
__url__ = "http://roughingit.subtlehints.net/code/"
__description__ = "Creates a Yahoo style navigation"

SEPERATOR=' &#187;\n'

from Pyblosxom import tools
import os, string

class BreadCrumbs:
    def __init__(self, request):
        self._request = request
        self._crumbs = ''

    def __str__(self):
        self.littleCrumbs()
        return str(self._crumbs)

    def littleCrumbs(self):
        conf = self._request.getConfiguration()
        data = self._request.getData()

        #path = string.replace(data['root_datadir'], conf['datadir'], '')
        #crumblets = path.split(os.sep)
        # make breadcrumbs work with both category and calendar url's
        # e.g. /weblog/category/entry and /weblog/2004/11
        crumblets = data['path_info']
        if not crumblets:
            crumblets = []
            if data['pi_yr']: crumblets.append(data['pi_yr'])
            if data['pi_mo']: crumblets.append(data['pi_mo'])
            if data['pi_da']: crumblets.append(data['pi_da'])
            crumblets.append('index')
        path = os.sep + os.sep.join(crumblets)

        path_data = []

        # add the root of the weblog to the breadcrumbs
        if path == "/":
            pass
            #path_data.append('home')
        else:
            path_data.append('<a href="%s/">Blog</a>' % conf['base_url'])

        if len(crumblets) > 0:
            crumbs = ''
            for mem in crumblets:
                if mem:
                    crumbs += '/%s' % mem
                    if crumbs != path:
                        path_data.append('<a href="%s/">%s</a>' % (crumbs, mem.capitalize()))
                    elif data['root_datadir'].endswith('.txt'):
                        infile = file(data['root_datadir'])
                        title = infile.readline().strip()
                        infile.close()
                        path_data.append('<a href="%s.html">%s</a>' % (crumbs, title))
            self._crumbs = '<div class="blosxomBreadcrumbs">\n%s\n</div>' % SEPERATOR.join(path_data)


def cb_prepare(args):
    request = args['request']
    http = request.getHttp()
    data = request.getData()
    entry_list = data['entry_list']

    if http["PATH_INFO"].startswith("/static") or len(entry_list) == 0:
        return
    else:
        data["breadcrumbs"] = BreadCrumbs(request)


def cb_end(args):
    request = args['request']
    data = request.getData()
    if "breadcrumbs" in data:
        del data["breadcrumbs"]



