import os


class Config:
    # SECRET_KEY = appConfig['app']['secret'].get() or os.urandom(24)
    # WORKER_KEY = appConfig['app']['worker'].get()

    # Flash-SQLAlchemy config params
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:220384@5432/lct2022_service'
    SQLALCHEMY_TRACK_MODIFICATIONS = False