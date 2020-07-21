import transaction
import horseman.meta
import roughrider.routing.node

from collections import defaultdict
from autoroutes import Routes
from horseman.prototyping import Environ, StartResponse
from uvc_serviceportal.request import Request


class Application(
        horseman.meta.SentryNode,
        roughrider.routing.node.RoutingNode):

    __slots__ = ("_plugins", )

    def __init__(self):
        self.routes = Routes()
        self.hooks = defaultdict(list)
        self._plugins = {}

    def __setitem__(self, name, item):
        self._plugins[name] = item

    def __getitem__(self, name):
        return self._plugins[name]

    def __contains__(self, name):
        return name in self._plugins

    def __iter__(self):
        return iter(self._plugins)

    def listen(self, name: str):
        def wrapper(func):
            self.hooks[name].append(func)
        return wrapper

    def hook(self, name: str, *args, **kwargs):
        for func in self.hooks[name]:
            result = func(*args, **kwargs)
            if result:  # Allows to shortcut the chain.
                return result

    def handle_exception(self, exc_info, environ):
        transaction.abort()
        exc_type, exc, traceback = exc_info
        self['logger'].debug(exc)

    @staticmethod
    def request_factory(app, environ, **params):
        request = Request(app, environ, **params)
        app.hook('request_created', request=request)
        return request

    def __call__(self, environ: Environ, start_response: StartResponse):
        txn = transaction.begin()
        self.hook('transaction_begin', transaction=txn)

        def transaction_start_response(status, headers, exc_info=None):
            if exc_info is not None:
                transaction.abort()
            else:
                transaction.commit()
            return start_response(status, headers, exc_info)

        yield from super().__call__(environ, transaction_start_response)


app = Application()
