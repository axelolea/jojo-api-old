from flask import Blueprint, jsonify, request
from src.utils.database import db
from src.models.Parts import Part
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

countries = Blueprint('countries', __name__, url_prefix = '/api/v1/countries')


@countries.get('/')
def get_parts():
    parts_data = Part.query.all()
    parts_list = list()
    for part in parts_data:
        parts_list.append()
    return jsonify({
        'data': parts_list
        }), HTTP_200_OK