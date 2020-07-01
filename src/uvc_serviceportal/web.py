import horseman.meta
import horseman.response
import roughrider.routing.node
from roughrider.routing.route import add_route as route
from .layout import template_endpoint
from .leikas import leika1, REG
from uvc_serviceportal import ROUTES




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


@route(ROUTES, '/')
@template_endpoint('index.pt')
def index(request):
    return {'request': request, 'leikas': REG}
