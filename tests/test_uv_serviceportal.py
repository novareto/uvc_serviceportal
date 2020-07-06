#!/usr/bin/env python

"""Tests for `uv_serviceportal` package."""

import pytest
import unittest




def test_content(app):
    assert(1 is 1)


def test_index(app):
    from webtest import TestApp
    app =  TestApp(app)
    resp = app.get('/')
    assert(resp.status == '200 OK')
    assert(resp.mustcontain(u"UVC-Service Portal") is None)
