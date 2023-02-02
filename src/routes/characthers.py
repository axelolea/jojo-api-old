from flask import Blueprint, jsonify, request
from src.utils.database import db, Character
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from src.constants.default_params import INITIAL_PAGE, DEFAULT_CHARACTERS_PER_PAGE, MIN_CHARACTERS_PER_PAGE, MAX_CHARACTERS_PER_PAGE

characters = Blueprint('characters', __name__, url_prefix = '/api/v1/characters')


@characters.get('/')
def get_characters():

    page = request.args.get('page', INITIAL_PAGE, type=int)
    per_page = request.args.get('page', DEFAULT_CHARACTERS_PER_PAGE, type=int)

    characters_data = Character.query.all.paginate(page = page, per_page = per_page)

    data = list()

    for item in characters_data:
        
        pass
    # parts_data = Character.query.all()
    # parts_list = list()
    # for part in parts_data:
    #     parts_list.append(part)
    return jsonify({
        'message': 'hola'
        }), HTTP_200_OK


@characters.post('/')
def post_characters():
    # parts_data = Character.query.all()
    # parts_list = list()
    # for part in parts_data:
    #     parts_list.append(part)
    return jsonify({
        'message': 'hola'
        }), HTTP_200_OK