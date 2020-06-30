import hydra
import logging
import bjoern
import fanstatic
import pathlib
import rutter.urlmap
import horseman.auth
import horseman.response
import cromlech.session
import cromlech.sessions.file

from adhoc.db import Database, Collection
from adhoc.emailer import SecureMailer
from adhoc.storage import Storage
from adhoc.request import Request
from adhoc.auth import Auth, AuthNode
from adhoc.web import Website
from adhoc import ck_t
import code


logger = logging.getLogger(__name__)


def setup_app(config, logger):
    # setup_logbook(config.logging).push_application()
    storage = Storage(**dict(config.storage))

    # Preparing the overhead
    db = Database(**dict(config.db))
    request_factory = Request.factory(db, session_key="sess")

    # Add test users
    users = db.get(Collection.users)
    if "0101010001" not in users:
        user = users.createDocument()
        user['username'] = "0101010001"
        user['password'] = "password"
        user._key = "0101010001"
        user.save()

    # Web frontend
    emailer = SecureMailer(**dict(config.smtp))
    frontend = Website(emailer, storage, logger, request_factory, config)
    frontend.models.load()

    return frontend 




@hydra.main(config_path="config.yaml")
def run(config):
    # print(config.pretty())
    app = setup_app(config, logger)
    req = app.request_factory(None,{'sess':'tt', 'REQUEST_METHOD': 'GET'})
    banner = (
        "AdHoc DebugPrompt.\n"
        "The 'request' variable contains an empty request.\n"
        "The 'db' variable points to the Database "
        "'App' is the instance of the website.")
    globals_ = {
        'request': req,
        'db': req.db,
        'app': app}
    code.interact(banner=banner, local=globals_)



if __name__ == "__main__":
    run()
