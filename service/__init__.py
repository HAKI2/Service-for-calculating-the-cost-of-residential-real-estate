from flask import Flask
from config import Config
from service.extensions import db, migrate
from service.excel_import import blueprint as excel_bp
from service.database.models import user, request_pool, flat, analogue_flat, analogue_flat_corr, wall_material, \
    condition, segment



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db, app.config['MIGRATION_DIR'])
    app.register_blueprint(excel_bp)
    return app
