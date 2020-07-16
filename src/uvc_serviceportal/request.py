from dataclasses import dataclass
from horseman.meta import Overhead
import horseman.parsing
from urllib.parse import parse_qs, urlparse
from onelogin.saml2.auth import OneLogin_Saml2_Auth


@dataclass
class User:
    data: dict


class Request(Overhead):

    __slots__ = (
        'app', 'environ', 'params', 'session', 'data', 'method',
        'content_type', '_query', '_saml_environ', '_user'
    )

    def __init__(self, app, environ, session, **params):
        self.app = app
        self.environ = environ
        self.params = params
        self.data = None
        self.session = session
        self._user = ...
        self._query = None
        self._saml_environ = None
        self.method = environ['REQUEST_METHOD']
        if self.method in ('POST', 'PATCH', 'PUT'):
            self.content_type = environ.get('CONTENT_TYPE')
        else:
            self.content_type = None

    @classmethod
    def factory(cls, session_key):
        def request_factory(app, environ, **args):
            session = environ[session_key]
            return cls(app, environ, session, **args)
        return request_factory

    def set_data(self, data):
        self.data = data

    @property
    def mq_transaction(self):
        return self.app.mqcenter.get_transaction(self.app.config['mq_url'])

    @property
    def query(self):
        if self._query is None:
            if not 'QUERY_STRING' in self.environ:
                self._query = {}
            else:
                parsed_qs = parse_qs(
                self.environ['QUERY_STRING'], keep_blank_values=True)
                self._query = horseman.http.Query(parsed_qs).to_dict()
        return self._query

    @property
    def saml_environ(self):
        if self._saml_environ is not None:
            return self._saml_environ

        if self.data is None and self.content_type:
            form, files = horseman.parsing.parse(
                self.environ['wsgi.input'], self.content_type)
            self.set_data({
                'form': form.to_dict(),
                'files': files.to_dict()
            })
        else:
            self.set_data({'form': {}, 'files': {}})

        url_data = urlparse('{}://{}'.format(
            self.environ['wsgi.url_scheme'], self.environ['HTTP_HOST']))

        https = self.environ['wsgi.url_scheme'] == 'https'
        self._saml_environ = {
            'https': 'on' if https else 'off',
            'http_host': url_data.hostname,
            'server_port': url_data.port,
            'script_name': self.environ['SCRIPT_NAME'],
            'get_data': self.query,
            'post_data': self.data['form'],
            # Uncomment if using ADFS as IdP,
            # https://github.com/onelogin/python-saml/pull/144
            # 'lowercase_urlencoding': True,
        }
        return self._saml_environ

    def saml_auth(self):
        return OneLogin_Saml2_Auth(
            self.saml_environ, custom_base_path=self.app.saml_root)

    @property
    def user(self):
        if self._user is not ...:
            return self._user
        if 'samlUserdata' in self.session:
            self._user = User(data=self.session['samlUserdata'])
        else:
            self._user = None
        return self._user

    @classmethod
    def factory(cls, session_key):
        def request_factory(app, environ, **args):
            session = environ[session_key]
            return cls(app, environ, session, **args)
        return request_factory
