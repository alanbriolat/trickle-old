import sys

import web
from web import form

from trickle.delugeclient import DelugeClient

urls = (
    '/',    'index',
    '/([0-9a-f]+)', 'torrentinfo',
)

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
render = web.template.render('templates/', base='layout')

client = None


TORRENT_KEYS = []


class index:
    def GET(self):
        client.keepalive()
        status = client.web.update_ui(TORRENT_KEYS, {})
        print status
        return render.index(status)


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
