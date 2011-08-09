from deluge.ui.client import client

client.set_core_uri()

import web
from web import form

urls = (
    '/',    'index',
)

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
render = web.template.render('templates/', base='layout')


class index:
    def GET(self):
        return render.index(client.get_session_state())


if __name__ == '__main__':
    app.run()
