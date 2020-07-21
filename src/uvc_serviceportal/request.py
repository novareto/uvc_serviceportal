import horseman.meta
import horseman.parsing

from dataclasses import dataclass
from lazy import lazy
from urllib.parse import parse_qs, urlparse
from onelogin.saml2.auth import OneLogin_Saml2_Auth


@dataclass
class User:
    data: dict


class Request(horseman.meta.Overhead, dict):

    data: dict = None

    __slots__ = ('method', )

    def __init__(self, app, environ, **params):
        self.app = app
        self.environ = environ
        self.params = params
        self.method = environ['REQUEST_METHOD']

    @lazy
    def content_type(self):
        if self.method in ('POST', 'PATCH', 'PUT'):
            return environ.get('CONTENT_TYPE')

    @lazy
    def query(self):
        if not 'QUERY_STRING' in self.environ:
            return {}

        parsed_qs = parse_qs(
            self.environ['QUERY_STRING'], keep_blank_values=True)
        return horseman.http.Query(parsed_qs).to_dict()

    @lazy
    def saml_environ(self):
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
        return {
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

    @lazy
    def user(self):
        session = self['session']
        if 'samlUserdata' in session:
            return User(data=session['samlUserdata'])

    def set_data(self, data):
        self.data = data

    def saml_auth(self):
        return OneLogin_Saml2_Auth(
            self.saml_environ, custom_base_path=self.app['saml'])
