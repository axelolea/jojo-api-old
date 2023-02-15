from flask import Blueprint, jsonify, request
from jojo.utils.database import db, Part
from jojo.constants.http_status_codes import (
    HTTP_200_OK, 
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST, 
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from jojo.logic.list_content import list_part

parts = Blueprint('parts', __name__, url_prefix = '/api/v1/parts')

from jojo.constants.default_values import get_response

from jojo.logic.custom_validators import part_validator

@parts.get('')
def get_parts():
    parts_data = Part.query.all()
    parts_list = list()
    for part in parts_data:
        parts_list.append(list_part(part))
    return get_response(
        HTTP_200_OK,
        data = parts_list
    )

@parts.get('/<int:id>')
def get_part_id(id):
    part = Part.query.filter_by(id = id).first()
    if not part:
        return get_response(
            HTTP_404_NOT_FOUND,
            msg = 'Part not Founded'
        )
    return get_response(
        HTTP_200_OK,
        data = list_part(part)
    )

@parts.post('')
def post_parts():
    try:
        body = part_validator(request.json)
        # name = request.get_json().get('name')
        # number = request.get_json().get('number')
        # japanese_name = request.get_json().get('japanese_name')
        # romanization_name = request.get_json().get('romanization_name')
        # alther_name = request.get_json().get('alther_name')

        part = Part(
                    name = body.get('name') ,
                    number = body.get('number'),
                    japanese_name = body.get('japanese_name'),
                    romanization_name = body.get('romanization_name'),
                    alther_name = body.get('alther_name')
                )
        db.session.add(part)
        db.session.commit()
    except ValueError as e:
        return get_response(
            HTTP_400_BAD_REQUEST,
            msg = 'Argumentos invalidos'
        )
    except:
        return get_response(
            HTTP_500_INTERNAL_SERVER_ERROR
        ) 
    else:
        return get_response(
            HTTP_201_CREATED,
            data = list_part(part),
            msg = 'Post part created successfully'
        )
