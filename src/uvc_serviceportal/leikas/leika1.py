# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de


from uvc_serviceportal.leikas import REG
from uvc_serviceportal.components import BaseFormularObject


class Leika1(BaseFormularObject):
    pass


REG["leika1"] = Leika1(
    id="leika1",
    title=u"Leika Test",
    description="Leika Test Description",
    schema=None,
    output="<xml><uv></uv>",
    icon="bi bi-chevron-right",
)
