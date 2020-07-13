import pytest


@pytest.fixture
def app(caplog):
    from uvc_serviceportal.web import Application
    from uvc_serviceportal.request import Request
    from uvc_serviceportal import ROUTES
    from uvc_serviceportal.mq import MQCenter

    mqcenter = MQCenter({})
    return Application(
        mqcenter, caplog, Request, config={
            'mq_url': 'memory:///'
        }
    )


@pytest.fixture
def wsgiapp(app):
    from webtest import TestApp
    return TestApp(app)


@pytest.fixture
def reader():
    import socket
    from kombu.utils import nested
    from kombu import Queue, Consumer, Connection as AMQPConnection

    class Reader:

        def __init__(self):
            self.messages = []

        def callback(self, body, message):
            import pdb
            pdb.set_trace()
            self.messages.append(body, message)
            message.ack()

        def __call__(self, app):
            with AMQPConnection(app.config['mq_url']) as conn:
                queue = app.mqcenter.queues['info']
                with conn.Consumer(
                        queue, callbacks=[self.callback]) as consumer:
                    while True:
                        try:
                            conn.drain_events(timeout=2)
                        except socket.timeout:
                            break
            return self.messages

    return Reader()
