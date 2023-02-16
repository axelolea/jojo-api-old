from flask_restx import Namespace, Resource
from structlog import get_logger

logger = get_logger(__name__)

parts_namespace = Namespace('parts')

class Parts(Resource):
    def get(self):
        logger.debug('Parts.GET')
        return {
            'message': 'hello'
        }


parts_namespace.add_resource(Parts, '')