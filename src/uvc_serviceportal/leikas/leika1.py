# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de

from uvc_serviceportal.layout import template_endpoint
from uvc_serviceportal import ROUTES
from uvc_serviceportal.leikas import REG
from uvc_serviceportal.components import BaseFormularObject
from uvc_serviceportal.resources import app, vendor 
from autoroutes import Routes
from roughrider.routing.route import add_route as route


class Leika1(BaseFormularObject):
    pass





REG["leika1"] = Leika1(
    id="leika1",
    title=u"Leika Test",
    description="Leika Test Description",
    schema=SCHEMA,
    output="<xml><uv></uv>",
    icon="bi bi-chevron-right",
)


@route(ROUTES, '/leika1')
@template_endpoint('form.pt')
def index(request):
    #vendor.need()
    #app.need()
    import pdb; pdb.set_trace()
    return {'request': request, 'leika': REG['leika1']}
