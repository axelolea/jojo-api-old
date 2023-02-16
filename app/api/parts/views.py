from flask_restplus import Namespace, Resource
from structlog import get_logger

logger = get_logger(__name__)


parts_namespace = Namespace('parts')


class Parts(Resource):
    def get(self):
        pass


parts_namespace.add_resource(Parts, '')