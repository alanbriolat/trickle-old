import jsonrpclib


class DelugeClient(jsonrpclib.Server):
    def __init__(self, host='localhost', port=8112, password='deluge'):
        jsonrpclib.config.version = 1.0
        jsonrpclib.Server.__init__(self, 'http://%s:%s/json' % (host, port))
        self.auth.login(password)
