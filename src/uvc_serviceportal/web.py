import transaction
import horseman.meta
import horseman.response
import roughrider.routing.node

from horseman.prototyping import Environ, StartResponse
from roughrider.routing.route import add_route as route
from uvc_serviceportal import ROUTES

from .mq import MQTransaction, Message
from .layout import template_endpoint
from .leikas.components import REGISTRY


class Application(horseman.meta.SentryNode,
                  roughrider.routing.node.RoutingNode):

    __slots__ = (
        'mqcenter', 'config', 'logger', 'request_factory'
    )

    def __init__(self, mqcenter, logger, request_factory, config):
        self.request_factory = request_factory
        self.config = config
        self.logger = logger
        self.routes = ROUTES
        self.mqcenter = mqcenter

    def handle_exception(self, exc_info, environ):
        exc_type, exc, traceback = exc_info
        self.logger.debug(exc)

    def __call__(self, environ: Environ, start_response: StartResponse):
        with transaction.manager as txn:
            environ['txn'] = txn
            yield from super().__call__(environ, start_response)


@route(ROUTES, '/')
@template_endpoint('index.pt')
def index(request):
    return {
        'request': request,
        'leikas': REGISTRY,
        'leikas_json': REGISTRY.json()
    }


@route(ROUTES, '/whowhat/{leika_id:string}')
@template_endpoint('whowhat.pt')
def whowhat(request):
    if leika := REGISTRY.get(request.params["leika_id"]):
        if leika.security_level == 'Q1':
            location = 'http://localhost:8090/leikas/%s' % request.params["leika_id"]
            return horseman.response.reply(307, headers = dict(location=location))
        else:
            return {
                'request': request,
                'leika': leika,
                'leika_json': leika.json()
            }
    return horseman.response.reply(404)




@route(ROUTES, '/fail')
def failing(request):
    raise NotImplementedError('AAhhhh')
