import hydra
import logging
import bjoern
import pathlib
import fanstatic
import rutter.urlmap
import horseman.response
import cromlech.session
import cromlech.sessions.file

from uvc_serviceportal.request import Request
from uvc_serviceportal.web import Application


logger = logging.getLogger(__name__)


def setup_session(config):
    # Session middleware
    current = pathlib.Path(__file__).parent
    folder = current / "sessions"
    handler = cromlech.sessions.file.FileStore(folder, 300)
    manager = cromlech.session.SignedCookieManager("secret", handler, cookie="my_sid")
    return cromlech.session.WSGISessionManager(manager, environ_key="sess")


def setup_app(config, logger):
    frontend = Application(logger, Request, config)

    # Creating the main router
    application = rutter.urlmap.URLMap(
        not_found_app=horseman.response.Response.create(404)
    )
    application["/"] = frontend
    return application


@hydra.main(config_path="config.yaml")
def run(config):

    application = setup_app(config, logger)
    session = setup_session(config)

    # Serving the app
    server = config.server
    host, port = server.host, server.port
    logger.info(f"Server Started on http://{host}:{port}")
    bjoern.run(
        fanstatic.Fanstatic(session(application)),
        host, int(port), reuse_port=True,
    )


if __name__ == "__main__":
    run()
