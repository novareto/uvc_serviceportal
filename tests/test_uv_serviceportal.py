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
