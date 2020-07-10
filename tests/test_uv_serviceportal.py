#!/usr/bin/env python

"""Tests for `uv_serviceportal` package."""

import pytest
import unittest


def test_content(app):
    assert(1 is 1)


def test_index(wsgiapp):
    resp = wsgiapp.get('/')
    assert(resp.status == '200 OK')
    assert(resp.mustcontain("UVC-Service Portal") is None)


def test_registry():
    from uvc_serviceportal.leikas import BaseFormularObject
    from uvc_serviceportal.leikas import REGISTRY

    assert REGISTRY == {}
    REGISTRY.load()
    assert 'leika1' in REGISTRY

    with pytest.raises(ValueError):
        REGISTRY.register('test', object())

    class Test(BaseFormularObject):
        pass

    test = Test(id='test', title='test', description='test', jsonschema='{}', output='', icon='')
    REGISTRY.register('test', test)


def test_mq_send(app, reader):
    import kombu
    import transaction
    from uvc_serviceportal.mq import Message

    app.mqcenter.exchanges['test'] = kombu.Exchange('test', type='direct')
    app.mqcenter.register_queue('test', 'info', 'default')
    request = app.request_factory(app, environ={'REQUEST_METHOD': 'GET'})

    message = Message(type='info', data="BLA")
    with transaction.manager:
        with request.mq_transaction as dm:
            dm.createMessage(message)

    messages = reader(app)
