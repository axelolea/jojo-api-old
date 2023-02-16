from os import environ

class BaseConfig:
    TESTING = False
    SECRET_KEY = environ.get("SECRET_KEY"),
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    FLASK_DEBUG=1
    FLASK_RUN_PORT=5000

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DB_URI"),
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:admin@localhost/jojosdb'
class TestingConfig(BaseConfig):
    TESTING = True,
    SQLALCHEMY_DATABASE_URI = environ.get("TEST_DB_URI"),
