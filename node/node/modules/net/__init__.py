from .models import db
from .router import router

def install(app):
    db.init_app(app)
    with app.app_context():
        db.create_all(bind='net')
    app.register_blueprint(router, url_prefix='/net')
