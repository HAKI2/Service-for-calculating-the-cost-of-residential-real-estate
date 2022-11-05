from flask import Flask
from config import Config
from service.extensions import db, migrate, login
from service.excel_import import blueprint as excel_bp
from service.admin import blueprint as admin_bp
from service.database.models import user, request_pool, flat, analogue_flat, analogue_flat_corr, wall_material, \
    condition, segment
from service.admin import admin as fl_admin


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db, app.config['MIGRATION_DIR'])
    app.register_blueprint(excel_bp)
    app.register_blueprint(admin_bp)
    login.init_app(app)
    login.login_view = 'admin_base.login'
    login.login_message = 'Пожалуйста, авторизуйтесь, чтобы получить доступ к этой странице'
    login.login_message_category = 'info'
    fl_admin.init_app(app, db)
    return app

