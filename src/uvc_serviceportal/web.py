import transaction
import horseman.meta
import roughrider.routing.node

from horseman.prototyping import Environ, StartResponse
from roughrider.routing.route import add_route as route
from uvc_serviceportal import ROUTES

from .layout import template_endpoint
from .leikas.components import REGISTRY


class TestDataManager:

    def tpc_vote(self, txn):
        pass

    def tpc_begin(self, txn):
        print('Transaction commit begins.')

    def commit(self, txn):
        print('Transaction commiting !')

    def tpc_finish(self, txn):
        print('Transaction commit closing.')

    def abort(self, txn):
        print('Transaction aborted !')


class Application(horseman.meta.SentryNode,
                  roughrider.routing.node.RoutingNode):

    __slots__ = (
        'config', 'logger', 'request_factory'
    )

    def __init__(self, logger, request_factory, config):
        self.request_factory = request_factory
        self.config = config
        self.logger = logger
        self.routes = ROUTES

    def handle_exception(self, exc_info, environ):
        exc_type, exc, traceback = exc_info
        self.logger.debug(exc)

    def __call__(self, environ: Environ, start_response: StartResponse):
        with transaction.manager as tr:
            #tr.join(TestDataManager())
            yield from super().__call__(environ, start_response)


@route(ROUTES, '/')
@template_endpoint('index.pt')
def index(request):
    return {
        'request': request,
        'leikas': REGISTRY,
        'leikas_json': REGISTRY.json()
    }


@route(ROUTES, '/fail')
def failing(request):
    raise NotImplementedError('AAhhhh')
