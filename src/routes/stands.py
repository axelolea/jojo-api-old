from flask import Blueprint, jsonify

stands = Blueprint('stands', __name__, url_prefix = '/api/v1/stands')

@stands.get('/')
def get_stands():
    return jsonify({
        'message': 'Hola stands'
    })