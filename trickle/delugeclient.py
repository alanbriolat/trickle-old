import jsonrpclib


class DelugeClient(jsonrpclib.Server):
    def __init__(self, host='localhost', port=8112, password='deluge'):
        self._password = password
        jsonrpclib.config.version = 1.0
        jsonrpclib.Server.__init__(self, 'http://%s:%s/json' % (host, port))
        self.auth.login(self._password)

    def keepalive(self):
        self.auth.login(self._password)
