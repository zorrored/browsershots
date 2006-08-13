"""
Generate links for RSS and Atom feeds.
"""


def cb_prepare(args):
    request = args['request']
    conf = request.getConfiguration()
    # http = request.getHttp()
    data = request.getData()

    path = data['path_info'][:]
    if path:
        path.pop(-1)
    path = '/'.join(path)
    if path:
        path = '/' + path

    base_url = conf['base_url']
    feedlinks = []
    feedlinks.append('<link rel="alternate" type="application/rss+xml" href="%s%s/index.rss20" />' % (base_url, path))
    feedlinks.append('<link rel="alternate" type="application/atom+xml" href="%s%s/index.atom" />' % (base_url, path))
    data["feedlinks"] = '\n'.join(feedlinks)

    base_url = base_url.replace(':', '%3A')
    feedvalidators = []
    feedvalidators.append('<a href="http://feedvalidator.org/check.cgi?url=%s%s/index.rss20"><img src="/static/rss20.png" alt="Valid RSS 2.0" /></a>' % (base_url, path))
    feedvalidators.append('<a href="http://feedvalidator.org/check.cgi?url=%s%s/index.atom"><img src="/static/atom.png" alt="Valid Atom" /></a>' % (base_url, path))
    data["feedvalidators"] = '<br />\n'.join(feedvalidators)


def cb_end(args):
    request = args['request']
    data = request.getData()
    if "feedlinks" in data:
        del data["feedlinks"]
    if "feedvalidators" in data:
        del data["feedvalidators"]
