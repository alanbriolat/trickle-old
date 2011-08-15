from trickle.jsonrpc import ServerProxy


class DelugeClient(ServerProxy):
    def __init__(self, host='localhost', port=8112, password='deluge'):
        self._password = password
        super(DelugeClient, self).__init__('http://%s:%s/json' % (host, port))
        self.auth.login(self._password)

    def keepalive(self):
        self.auth.login(self._password)
