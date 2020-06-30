import hydra
import logging
import bjoern
import pathlib
import rutter.urlmap
import horseman.response

from adhoc.request import Request
from adhoc.web import Application


logger = logging.getLogger(__name__)


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

    # Serving the app
    server = config.server
    host, port = server.host, server.port
    logger.info(f"Server Started on http://{host}:{port}")
    bjoern.run(
        application,
        host, int(port), reuse_port=True,
    )


if __name__ == "__main__":
    run()
