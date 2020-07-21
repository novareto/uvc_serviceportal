def Session(app, config):

    folder = hydra.utils.to_absolute_path(config.sessions.folder)
    handler = cromlech.sessions.file.FileStore(folder, 3600)
    manager = cromlech.session.SignedCookieManager(
        "secret", handler, cookie="my_sid")

    @app.listen('request_created')
    def session(request):
        request['session'] = request.environ[config.sessions.environ_key]

    return cromlech.session.WSGISessionManager(
        manager, environ_key=config.app.session_key)(app)
