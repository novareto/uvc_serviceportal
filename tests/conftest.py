import pytest


@pytest.fixture
def app(caplog):
    from uvc_serviceportal.app import Application
    from uvc_serviceportal.mq import MQCenter

    app = Application()
    mqcenter = MQCenter('memory:///')
    app['mq'] = mqcenter
    return app


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
            self.messages.append(body)
            message.ack()

        def __call__(self, app):
            with AMQPConnection(app['mq'].url) as conn:
                queue = app['mq'].queues['info']
                with conn.Consumer(
                        [queue], callbacks=[self.callback]) as consumer:
                    while True:
                        try:
                            conn.drain_events(timeout=1)
                        except socket.timeout:
                            break
            return self.messages

    return Reader()
