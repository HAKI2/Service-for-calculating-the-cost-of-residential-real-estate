import os
import yaml

with open("config.yaml", "r") as f:
    try:
        appConfig = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print(exc)


class Config:
    SECRET_KEY = appConfig['app']['secret']
    ADMIN_PASSWORD = appConfig['app']['admin_password']
    ADMIN_EMAIL = appConfig['app'].get('admin_email')
    # WORKER_KEY = appConfig['app']['worker'].get()

    POSITION_STACK_API = appConfig['api'].get('position_stack_api')
    MAPBOX_API = appConfig['api'].get('mapbox_api')
    # Flash-SQLAlchemy config params
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(
        appConfig['db']['user'], appConfig['db']['pass'],
        appConfig['db']['host'], appConfig['db']['name'])
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # UPLOAD_FOLDER = UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])

    MIGRATION_DIR = os.path.join('service', 'database', 'migrations')
