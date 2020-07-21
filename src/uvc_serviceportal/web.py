import transaction
import horseman.meta
import horseman.response
import roughrider.routing.node

import uvc_serviceportal.saml
from .app import app
from .message import FlashMessages
from .mq import MQTransaction, Message
from .layout import template_endpoint
from .leikas.components import REGISTRY


@app.route("/")
@template_endpoint("index.pt")
def index(request):
    request['flash'].createMessage(body='Some message')
    return {
        'request': request,
        'leikas': REGISTRY,
        'leikas_json': REGISTRY.json()
    }


@app.route("/login")
@template_endpoint("login.pt")
def login(request):
    return {
        "request": request,
    }


@app.route("/whowhat/{leika_id:string}")
@template_endpoint("whowhat.pt")
def whowhat(request):
    if leika := REGISTRY.get(request.params["leika_id"]):
        if leika.security_level == "Q1" and request.user is None:
            return horseman.response.reply(
                code=307,
                headers={
                    "Location": "/saml/sso"
                })
        elif leika.security_level == "Q2":
            return horseman.response.reply(
                code=307,
                headers={
                    "Location": "/leikas/%s" % request.params["leika_id"]
                },
            )
    return horseman.response.reply(404)


@app.route("/fail")
def failing(request):
    raise NotImplementedError("AAhhhh")
