from horseman.meta import Overhead


class Request(Overhead):

    __slots__ = (
        'app', 'environ', 'params', 'data', 'method', 'content_type'
    )

    def __init__(self, app, environ, **params):
        self.app = app
        self.environ = environ
        self.params = params
        self.data = {}
        self.method = environ['REQUEST_METHOD']
        if self.method in ('POST', 'PATCH', 'PUT'):
            self.content_type = environ.get('CONTENT_TYPE')
        else:
            self.content_type = None

    def set_data(self, data):
        self.data = data

    @property
    def mq_transaction(self):
        return self.app.mqcenter.get_transaction(self.app.config['mq_url'])
