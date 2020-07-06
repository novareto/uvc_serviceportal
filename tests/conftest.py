# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de

import pytest


@pytest.fixture
def app(caplog):
    from uvc_serviceportal.web import Application
    from uvc_serviceportal.request import Request
    from uvc_serviceportal import ROUTES

    return Application(
        request_factory=Request, config=dict(), logger=caplog 
    )
