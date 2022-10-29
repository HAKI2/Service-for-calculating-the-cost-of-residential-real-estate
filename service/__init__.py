from flask import Flask
from config import Config
from service.extensions import db, migrate
from service.database.models import User


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db, app.config['MIGRATION_DIR'])
    return app


