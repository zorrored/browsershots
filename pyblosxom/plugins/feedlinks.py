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

    feedlinks = []
    feedlinks.append('<link rel="alternate" type="application/rss+xml"' +
                     ' href="%s%s/index.rss20" />' % (conf['base_url'], path))
    feedlinks.append('<link rel="alternate" type="application/atom+xml"' +
                     ' href="%s%s/index.atom" />' % (conf['base_url'], path))
    data["feedlinks"] = '\n'.join(feedlinks)


def cb_end(args):
    request = args['request']
    data = request.getData()
    if "feedlinks" in data:
        del data["feedlinks"]
