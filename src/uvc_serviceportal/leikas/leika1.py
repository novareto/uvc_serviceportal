# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de

from pathlib import Path
import horseman.parsing
import horseman.response
import horseman.meta
from uvc_serviceportal.layout import template_endpoint
from uvc_serviceportal import ROUTES
from uvc_serviceportal.leikas.components import REGISTRY
from uvc_serviceportal.leikas.components import BaseFormularObject
from uvc_serviceportal.resources import csc
from autoroutes import Routes
from roughrider.routing.route import add_route as route


PATH = Path(__file__)


class Leika1(BaseFormularObject):

    def __init__(self, *args, **kwargs):
        with PATH.with_suffix('.json').open() as fd:
            kwargs['jsonschema'] = fd.read()
        super().__init__(*args, **kwargs)

    @property
    def action(self):
        return "%s/add" % self.id


LEIKA = Leika1(
    id="leika1",
    title=u"Leika Test",
    description="Leika Test Description",
    output="<xml><uv><name>{name}</name></uv>",
    icon="bi bi-chevron-right",
)


@route(ROUTES, '/leikas/{leika_id:string}')
class Index(horseman.meta.APIView):

    @template_endpoint('form.pt')
    def GET(self, request):
        #csc.need()
        if leika := REGISTRY.get(request.params['leika_id']):
            return {'request': request, 'leika': leika}
        return horseman.response.reply(404)


@route(ROUTES, '/leikas/{leika_id:string}/add')
class Add(horseman.meta.APIView):

    def POST(self, request):
        form, files = horseman.parsing.parse(
            request.environ['wsgi.input'], request.content_type)
        if leika := REGISTRY.get(request.params['leika_id']):
            from repoze.filesafe import create_file
            f = create_file('/tmp/leik1.xml')
            f.write(leika.output.format(**form.to_dict()))
            import pdb; pdb.set_trace()
