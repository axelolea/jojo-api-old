from flask_restx import Api
from app.api.parts.views import parts_namespace
api = Api(version = '1.0.1', title = 'Jojo\'s API', doc="/api/v1/docs")
api.add_namespace(parts_namespace, path="/api/v1/parts")