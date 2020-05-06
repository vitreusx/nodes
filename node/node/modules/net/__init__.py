from .router import Router
from os import makedirs
from os.path import join, dirname
import shelve

def install(app, conf):
    path = join(app.root, conf.get('db') or 'db/net.db')
    makedirs(dirname(path), exist_ok=True)
    db = shelve.open(path, writeback=True)

    router = Router(conf, app.port, db)
    app.flask.register_blueprint(router.router, url_prefix='/net')
