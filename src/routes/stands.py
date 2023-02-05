from flask import Blueprint, jsonify, request

stands = Blueprint('stands', __name__, url_prefix = '/api/v1/stands')

@stands.get('/')
def get_stands():
    return jsonify({
        'message': 'Hola parts'
    })


@stands.post('/')
def post_stands():

    body = request.json

    return jsonify({
        'message': 'Hola parts'
    })