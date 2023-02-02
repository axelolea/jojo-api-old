from flask import Blueprint, jsonify, request
from src.utils.database import db, Part
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from src.logic.list_content import list_part

parts = Blueprint('parts', __name__, url_prefix = '/api/v1/parts')


@parts.get('/')
def get_parts():
    parts_data = Part.query.all()
    parts_list = list()
    for part in parts_data:
        parts_list.append(list_part(part))
    return jsonify({
        'data': parts_list
        }), HTTP_200_OK

@parts.get('/<int:id>')
def get_part_id(id):
    part = Part.query.filter_by(id = id).first()
    if not part:
        return jsonify({
            'message': f'Not found part with <id:{id}>'
            }), HTTP_404_NOT_FOUND
    return jsonify({
        'data': list_part(part)
        }), HTTP_200_OK

@parts.post('/')
def post_parts():
    name = request.get_json().get('name', None)
    number = request.get_json().get('number', None)
    japanese_name = request.get_json().get('japanese_name', None)
    romanization_name = request.get_json().get('romanization_name', None)
    alther_name = request.get_json().get('alther_name', None)
    if not (name and number and japanese_name and romanization_name):
        return jsonify({
            'error': 'Faltan parametros'
        }), HTTP_400_BAD_REQUEST
    part = Part(
                name = name,
                number = number,
                japanese_name = japanese_name,
                romanization_name = romanization_name,
                alther_name = alther_name
            )
    db.session.add(part)
    db.session.commit()
    return jsonify({
        'message': 'Post part created successfully',
        'data': {
            'name': part.name,
            'number': part.number
        }
    }), HTTP_201_CREATED
