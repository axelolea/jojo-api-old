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