# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de

from pathlib import Path
import horseman.parsing
import horseman.response
import horseman.meta
from uvc_serviceportal.app import app
from uvc_serviceportal.layout import template_endpoint, xml_endpoint
from uvc_serviceportal.leikas.components import REGISTRY
from uvc_serviceportal.leikas.components import BaseFormularObject
from uvc_serviceportal.resources import csc
from autoroutes import Routes
from uvc_serviceportal.mq import Message


PATH = Path(__file__)


class Leika1(BaseFormularObject):
    def __init__(self, *args, **kwargs):
        with PATH.with_suffix(".json").open() as fd:
            kwargs["jsonschema"] = fd.read()
        super().__init__(*args, **kwargs)

    @property
    def action(self):
        return "%s/add" % self.id


LEIKA = Leika1(
    id="leika1",
    title="Unfallanzeige",
    description="Elektronische Unfallanzeige",
    security_level="Q1",
    tags=["Unfall", "Sicherheitsfachkraft"],
    output="<xml><uv><name>{name}</name></uv>",
    icon="bi bi-chevron-right",
)


LEIKA1 = Leika1(
    id="leika2",
    title="Berufskrankheiten",
    description="Antrag auf Berufskrankheiten",
    security_level="Q2",
    tags=["Unfallanzeige", "Sicherheitsfachkraft"],
    output="<xml><uv><name>{name}</name></uv>",
    icon="bi bi-chevron-right",
)


@app.route("/leikas/{leika_id:string}")
class Index(horseman.meta.APIView):
    @template_endpoint("form.pt")
    def GET(self, request):
        # csc.need()
        if leika := REGISTRY.get(request.params["leika_id"]):
            return {"request": request, "leika": leika}
        return horseman.response.reply(404)


@app.route("/leikas/{leika_id:string}/add")
class Add(horseman.meta.APIView):
    @xml_endpoint("leika1.xml")
    def GET(self, request):
        if leika := REGISTRY.get(request.params["leika_id"]):
            return {"name": "My name"}
        return horseman.response.reply(404)

    def POST(self, request):
        form, files = horseman.parsing.parse(
            request.environ["wsgi.input"], request.content_type
        )
        if leika := REGISTRY.get(request.params["leika_id"]):
            with request.mq_transaction as mq:
                mq.createMessage(
                    Message(queue="info", routing_key="default", data="test")
                )
            # from repoze.filesafe import create_file
            # f = create_file('/tmp/leik1.xml')
            # f.write(leika.output.format(**form.to_dict()))
            # 1/0
