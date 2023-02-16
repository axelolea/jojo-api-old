from flask import Flask
from os import getenv
from flask_migrate import Migrate

# Database 
from flask_sqlalchemy import SQLAlchemy
from app.api import api
from structlog import get_logger
from flask_cors import CORS

logger = get_logger(__name__)

# Connection Database
db = SQLAlchemy()
cors = CORS()

def create_app(script_info = None):

    app = Flask(__name__, instance_relative_config=True)

    app_settings = getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    
    # Config database
    db.app = app
    db.init_app(app)

    migrate = Migrate(app, db)

    cors.init_app(app, resources={r"*": {"origins": "*"}})
    api.init_app(app)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app

