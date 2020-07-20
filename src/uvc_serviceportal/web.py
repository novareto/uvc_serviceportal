import transaction
import horseman.meta
import horseman.response
import roughrider.routing.node

from horseman.prototyping import Environ, StartResponse
from roughrider.routing.route import add_route as route

import uvc_serviceportal.saml
from uvc_serviceportal import ROUTES
from .message import FlashMessages
from .mq import MQTransaction, Message
from .layout import template_endpoint
from .leikas.components import REGISTRY

import wtforms.form
import wtforms.fields
import wtforms.validators
from horseman.parsing import parse


class Application(horseman.meta.SentryNode,
                  roughrider.routing.node.RoutingNode):

    __slots__ = ("mqcenter", "config", "logger", "request_factory")

    def __init__(self, mqcenter, logger, request_factory, config, saml_root):
        self.request_factory = request_factory
        self.config = config
        self.saml_root = saml_root
        self.logger = logger
        self.routes = ROUTES
        self.mqcenter = mqcenter

    def handle_exception(self, exc_info, environ):
        transaction.abort()
        exc_type, exc, traceback = exc_info
        self.logger.debug(exc)

    def __call__(self, environ: Environ, start_response: StartResponse):
        transaction.begin()

        def transaction_start_response(status, headers, exc_info=None):
            if exc_info is not None:
                transaction.abort()
            else:
                transaction.commit()
            return start_response(status, headers, exc_info)

        yield from super().__call__(environ, transaction_start_response)


@route(ROUTES, "/")
@template_endpoint("index.pt")
def index(request):
    with FlashMessages(request.session, 'messages') as fm:
        fm.createMessage('some message')
        return {
            'request': request,
            'leikas': REGISTRY,
            'messages': fm.hasMessages and fm.exhaustMessages() or None,
            'leikas_json': REGISTRY.json()
        }


@route(ROUTES, "/login")
@template_endpoint("login.pt")
def login(request):
    return {
        "request": request,
    }


@route(ROUTES, "/whowhat/{leika_id:string}")
@template_endpoint("whowhat.pt")
def whowhat(request):
    if leika := REGISTRY.get(request.params["leika_id"]):
        if leika.security_level == "Q2" and request.user is None:
            return horseman.response.reply(code=307, headers={"Location": "/saml/sso"})
        if leika.security_level == "Q2" and request.user is not None:
            return horseman.response.reply(
                code=307,
                headers={"Location": "/leikas/%s" % request.params["leika_id"]},
            )
        elif leika.security_level == "Q1":
            return horseman.response.reply(
                code=307,
                headers={"Location": "/leikas/%s" % request.params["leika_id"]},
            )
    return horseman.response.reply(404)


@route(ROUTES, "/fail")
def failing(request):
    raise NotImplementedError("AAhhhh")
