from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

def create_app():  # config_class=Config
    app = Flask(__name__)
    app.config.from_object(Config)
    db = SQLAlchemy(app)
    db = SQLAlchemy
    migrate = Migrate(app, db)
    return app