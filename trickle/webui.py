import sys

import web
from web import form

from trickle.delugeclient import DelugeClient

urls = (
    '/', 'index',
    '/torrent/([0-9a-f]+)', 'torrentinfo',
)

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
from trickle.templates import render

client = None


TORRENT_KEYS = []
SORT_SCHEMES = {
    'added_asc': ('time_added', False),
    'added_desc': ('time_added', True),
}

def sort_torrents(torrents, sort_order):
    field, reverse = sort_order
    return sorted(torrents, key=lambda t: t[field], reverse=reverse)


class index:
    def GET(self):
        client.keepalive()
        status = client.web.update_ui(TORRENT_KEYS, {})
        sort_order = SORT_SCHEMES.get(web.ctx.query[1:], SORT_SCHEMES['added_desc'])
        torrents = sort_torrents(status['torrents'].values(), sort_order)
        print status
        return render.index(status, torrents)


class torrentinfo:
    def GET(self, torrentid):
        client.keepalive()
        info = client.web.get_torrent_status(torrentid, TORRENT_KEYS)
        print info
        files = client.web.get_torrent_files(torrentid)
        print files
        return render.torrentinfo(info, files)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=8112, type=int)
    parser.add_argument('--password', default='deluge')
    parser.add_argument('--no-password', action='store_const',
                        const='', dest='password')
    args = parser.parse_args()

    client = DelugeClient(args.host, args.port, args.password)

    sys.argv[1:] = []
    app.run()
