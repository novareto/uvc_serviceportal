# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de

from pathlib import Path
from uvc_serviceportal.layout import template_endpoint
from uvc_serviceportal import ROUTES
from uvc_serviceportal.leikas import REG
from uvc_serviceportal.components import BaseFormularObject
from uvc_serviceportal.resources import csc
from autoroutes import Routes
from roughrider.routing.route import add_route as route


PATH = Path(__file__)


class Leika1(BaseFormularObject):

    def __init__(self, *args, **kwargs):
        with PATH.with_suffix('.json').open() as fd:
            kwargs['schema'] = fd.read()
        super().__init__(*args, **kwargs)


REG["leika1"] = Leika1(
    id="leika1",
    title=u"Leika Test",
    description="Leika Test Description",
    output="<xml><uv></uv>",
    icon="bi bi-chevron-right",
)


@route(ROUTES, '/leika1')
@template_endpoint('form.pt')
def index(request):
    #csc.need()
    return {'request': request, 'leika': REG['leika1']}
