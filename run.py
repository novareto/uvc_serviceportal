import os
import hydra
import hydra.utils
import kombu
import logging
import bjoern
import pathlib
import fanstatic
import transaction
import rutter.urlmap
import horseman.response
import cromlech.session
import cromlech.sessions.file

from uvc_serviceportal.app import app
from uvc_serviceportal.mq import MQCenter
from uvc_serviceportal.request import Request
from uvc_serviceportal.leikas.components import REGISTRY
from uvc_serviceportal.message import FlashMessageDataManager


import uvc_serviceportal.web


logger = logging.getLogger(__name__)


def setup_session(config):
    # Session middleware
    folder = hydra.utils.to_absolute_path(config.sessions.folder)
    handler = cromlech.sessions.file.FileStore(folder, 3600)
    manager = cromlech.session.SignedCookieManager(
        "secret", handler, cookie="my_sid")
    return cromlech.session.WSGISessionManager(
        manager, environ_key=config.sessions.environ_key)


def setup_app(config, logger):

    @app.listen('request_created')
    def session(request):
        request['session'] = request.environ[config.sessions.environ_key]

    @app.listen('request_created')
    def flash_messages(request):
        txn = transaction.get()
        dm = FlashMessageDataManager(request['session'], 'messages')
        txn.join(dm)
        request['flash'] = dm

    # Logger
    app['logger'] = logger

    # MQ
    mqcenter = MQCenter(config.app.mq_url, {
        'test': kombu.Exchange('test', type='direct')
    })
    mqcenter.register_queue('test', 'info', 'default')
    app['mq'] = mqcenter

    # SAML
    app['saml'] = hydra.utils.to_absolute_path(config.SAML.folder)

    # Creating the main router
    application = rutter.urlmap.URLMap(
        not_found_app=horseman.response.Response.create(404)
    )
    application["/"] = app
    return application


def setup_env(config):
    if config.templates.cache:
        cache_folder = pathlib.Path(hydra.utils.to_absolute_path(
            config.templates.cache))
        cache_folder.mkdir(mode=0o755, parents=False, exist_ok=True)
        os.environ['CHAMELEON_CACHE'] = str(cache_folder)
    if config.templates.debug:
        os.environ['CHAMELEON_DEBUG'] = 'true'


@hydra.main(config_path="config.yaml", strict=False)
def run(config):

    setup_env(config)
    session = setup_session(config)
    application = session(setup_app(config, logger))

    # Loading Leikas
    REGISTRY.load()

    # Serving the app
    server = config.server
    host, port = server.host, server.port
    logger.info(f"Server Started on http://{host}:{port}")
    bjoern.run(
        fanstatic.Fanstatic(application, bottom=True, compile=True),
        host,
        int(port),
        reuse_port=True,
    )


if __name__ == "__main__":
    run()
