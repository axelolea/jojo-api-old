from flask import Flask
from os import getenv

# Database 
from flask_sqlalchemy import SQLAlchemy
from structlog import get_logger
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

logger = get_logger(__name__)

# Connection Database
db = SQLAlchemy()
cors = CORS()

def create_app(script_info = None):

    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    app_settings = getenv('APP_SETTINGS')
    # from app.config import DevelopmentConfig
    # app_settings = DevelopmentConfig
    app.config.from_object(app_settings)
    
    # Config database
    db.app = app
    db.init_app(app)

    cors.init_app(app, resources={r"*": {"origins": "*"}})
    
    from app.api import api
    api.init_app(app)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
