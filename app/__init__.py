from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from . import routes, models
        db.create_all()
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(routes.admin_bp)

    return app