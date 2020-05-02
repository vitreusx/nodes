from .models import db, ma
from .router import Router
from os.path import join

def install(app, conf):
    path = join(app.root, conf.get('db') or 'db/net.db')
    app.ensure_fs(path)

    db_uri = f'sqlite:///{path}'
    app.flask.config['SQLALCHEMY_BINDS']['net'] = db_uri

    db.init_app(app.flask)
    ma.init_app(app.flask)
    with app.flask.app_context():
        db.create_all(bind='net')

    router = Router(db, conf)
    app.flask.register_blueprint(router.router, url_prefix='/net')
