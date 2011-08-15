"""An extremely simple JSON-RPC 1.0 client.

This JSON-RPC client implements just enough functionality to interact with the
JSON API of the Deluge bittorrent client over HTTP, including using cookies for
session identification.  It is probably missing important aspects that would
make it fully compliant with all JSON-RPC 1.0 servers."""

import json
import cookielib

import requests


class ServerProxy(object):
    """JSON-RPC server proxy for proxying calls to the interface at *uri*."""
    def __init__(self, uri):
        self._uri = uri
        self._cookies = cookielib.CookieJar()
        self._req_id = 1

    def __getattr__(self, name):
        """Attributes of the :class:`ServerProxy` correspond to methods of the
        JSON-RPC server."""
        return _Method(self, name)

    def _next_id(self):
        """Get a session-unique request identifier."""
        tmp = self._req_id
        self._req_id += 1
        return tmp

    def _request(self, method, params):
        """Proxy a method call to the JSON-RPC server, returning the result."""
        # Build the request object
        req_id = self._next_id()
        request = {'id': req_id,
                   'method': method,
                   'params': params}
        # Get the response
        response = requests.post(self._uri,
                                 json.dumps(request),
                                 cookies=self._cookies)
        # Raise exception if there was an error at the HTTP layer
        response.raise_for_status()
        # Decode response
        content = json.loads(response.content)
        # Raise exception if the response ID is wrong
        if content['id'] != req_id:
            raise ProtocolError('Request and response ID do not match')
        # Raise exception if there was an error from the JSON-RPC server
        if content['error']:
            raise ProtocolError(content['error'])
        # Return response data
        return content['result']


class ProtocolError(Exception):
    """A JSON-RPC protocol error."""
    pass


class _Method(object):
    """Magic class for :class:`ServerProxy` methods, allowing calls like
    ``server.foo.bar()``."""
    def __init__(self, proxy, name):
        self._proxy = proxy
        self._name = name

    def __getattr__(self, name):
        """A call to ``s.foo.bar`` makes a call to the ``foo.bar`` method on
        the JSON-RPC server."""
        return _Method(self._proxy, '%s.%s' % (self._name, name))

    def __call__(self, *args, **kwargs):
        """When the method is called, make a request to the server."""
        if kwargs:
            raise Exception('Keyword arguments not supported')
        return self._proxy._request(self._name, args)
