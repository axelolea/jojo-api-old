from flask import Flask
from os import environ
from src.utils.database import db
# Routes
from src.routes.characthers import characters
from src.routes.stands import stands
from src.routes.parts import parts
from src.routes.countries import countries

def create_app(test_config = None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY = environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS = False,
            JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY'),
        )
    else:
        app.config.from_mapping(test_config)
    
    # Config database
    db.app = app
    db.init_app(app)

    app.register_blueprint(characters)
    app.register_blueprint(stands)
    app.register_blueprint(parts)
    app.register_blueprint(countries)

    return app