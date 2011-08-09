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


TORRENT_KEYS = []


class index:
    def GET(self):
        c = DelugeClient()
        status = c.web.update_ui(TORRENT_KEYS, {})
        print status
        return render.index(status)


class torrentinfo:
    def GET(self, torrentid):
        c = DelugeClient()
        info = c.web.get_torrent_status(torrentid, TORRENT_KEYS)
        print info
        files = c.web.get_torrent_files(torrentid)
        print files
        return render.torrentinfo(info, files)


if __name__ == '__main__':
    app.run()
