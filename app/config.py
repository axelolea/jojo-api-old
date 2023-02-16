from os import environ

class BaseConfig:
    TESTING = False
    SECRET_KEY = environ.get("SECRET_KEY"),
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY'),

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DB_URI"),
class TestingConfig(BaseConfig):
    TESTING = True,
    SQLALCHEMY_DATABASE_URI = environ.get("TEST_DB_URI"),