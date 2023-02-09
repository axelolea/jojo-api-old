from flask import Blueprint, jsonify, request
from src.utils.database import db, Character, Image, Part, Stand, Country
from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR)
from src.logic.list_content import list_characters, list_images, list_pagination, list_character_basic
from src.constants.default_values import (
    INITIAL_PAGE,
    DEFAULT_CHARACTERS_PER_PAGE,
    MIN_CHARACTERS_PER_PAGE, 
    MAX_CHARACTERS_PER_PAGE,
    PARTS_IN_JOJOS)
# from src.logic.custom_validators import validate_country, validate_images, validate_list_type
from src.logic.custom_validators import validate_character, validate_params
# Create Blueprint 
characters = Blueprint('characters', __name__, url_prefix = '/api/v1/characters')


@characters.get('')
def get_characters():
    try:
        page = request.args.get('page', INITIAL_PAGE, type=int)
        per_page = request.args.get('per_page', DEFAULT_CHARACTERS_PER_PAGE, type=int)
        if not (per_page in range(MIN_CHARACTERS_PER_PAGE, MAX_CHARACTERS_PER_PAGE)):
            raise ValueError('Per Page is out of limit range')
        characters_data = Character.query.paginate(page = page, per_page = per_page)
        data = list()

        for item in characters_data:
            data.append(list_character_basic(item))

        return jsonify({
            'data': data,
            'pagination': list_pagination(characters_data)
            }), HTTP_200_OK
    except ValueError as e:
        return jsonify({
            'status': 400,
            'type': type(e).__name__,
            'message': e.args[0],
            "error": 'Uno de los parametros es incorrecto',
            }), HTTP_400_BAD_REQUEST


@characters.get('/<int:id>')
def get_character_id(id):
    character = Character.query.get(id)
    if not character:
        return jsonify({
            'message': f'Not found part with <id:{id}>'
            }), HTTP_404_NOT_FOUND
    return jsonify({
        'data': list_characters(character)
        }), HTTP_200_OK


@characters.post('')
def post_character():
    # <-- Params will created a character -->
    # +---------------+----------+----------+----------------------------------+
    # | Params        | Type     | Required | Description                      |
    # +---------------+----------+----------+----------------------------------+
    # | name          | str      | True     | Alphanumeric name.               |
    # | japanese_name | str      | True     | Name in katakana or kanji.       |
    # | alther_name   | str      | False    | Alther name (for CR Claim. etc). |
    # | parts         | list     | True     | List part aparization.           |
    # | living        | bool     | True     | Is actual living character, skip |
    # |               |          |          | reset universe of Pucchi.        |
    # | catchphrase   | str      | False    | Frecuency Use Slogan.            |
    # | is_human      | bool     | False    | Is human character.              |
    # | country_id    | int/str  | False    | Response a section with id       |
    # |               |          |          | country , code or name.          |
    # | images        | dict/obj | False    | Response with dictionary with    |
    # |               |          |          | contain a 2 min images.          |
    # +---------------+----------+----------+----------------------------------+
    # images:
    #           {
    #               "half_body" url with image [str] [null]
    #               "full_body" url with image [str] [null]
    #           }

    try:
        # Body with data params 
        body = validate_character(request.json)
        # Required params 

        name = body.get('name')
        japanese_name = body.get('japanese_name')
        parts = body.get('parts')
        country = body.get('country')
        # Set values or Default
        is_hamon_user = body.get('is_hamon_user', False)
        is_stand_user = body.get('is_stand_user', False)
        is_gyro_user = body.get('is_gyro_user', False)
        is_human = body.get('is_human', True)
        living = body.get('living', True)
        # Set values or Null 
        alther_name = body.get('alther_name')
        catchphrase = body.get('catchphrase')


        # Validar nacionalidad
        if country:
            if type(country) == int:
                country_q = Country.query.filter_by(id = country).first()
            else:
                country_q = Country.query.filter_by(country_code = country).first()
            if not country_q:
                raise ValueError(f'Not found country with {country} ID or Code')

        # Create Character 
        character = Character(
            name = name,
            alther_name = alther_name,
            japanese_name = japanese_name,
            catchphrase = catchphrase,
            is_hamon_user = is_hamon_user,
            is_stand_user = is_stand_user,
            is_gyro_user = is_gyro_user,
            living = living,
            is_human = is_human
        )

        # Set stand 
        if is_stand_user:
            for stand in body.get('stands'):
                if type(stand) == int:
                    get_stand = Stand.query.filter_by(id = stand).first()
                elif type(stand) == str:
                    get_stand = Stand.query.filter_by(name = stand).first()
                if not get_stand:
                    raise ValueError(f'Not found stand {stand}')
                character.stands_r.append(get_stand)
        # Validate images 
        new_images = Image()
        if body.get('images'):
            images = body.get('images')
            new_images = Image(full_body = images.get('full_body'),
                               half_body = images.get('half_body'))
            db.session.add(new_images)
            db.session.commit()
        # Append character with parts
        for number in parts:
            part = Part.query.filter_by(number = number).first()
            character.parts_r.append(part)
        # Add country and images 
        if country:
            character.country_id = country_q.id
        if new_images.id:
            character.images_id = new_images.id

        # Add Character in database
        db.session.add(character)
        db.session.commit()
            
    # <-- Exception Manager -->

    # <-- Value of params is invalid, Exception ( message ) -->
    except ValueError as e:
        return jsonify({
        'status': 400,
        'type': type(e).__name__,
        'message': e.args[0],
        'error': 'Uno de los parametros es incorrecto',
        }), HTTP_400_BAD_REQUEST
    # <-- General exception error return -->
    except:
        return jsonify({
        'status': 500,
        'type': 'ServerError',
        "error": 'Problemas internos D:',
        }), HTTP_500_INTERNAL_SERVER_ERROR
    # <-- Send data of character created and status 201 [Created] -->
    else:
        return jsonify({
            'status': 201,
            'message': f'Character: {character.name} is created successfully',
            'data': list_characters(character)
            }), HTTP_201_CREATED

from src.logic.query import query_characters

@characters.get('/query')
def query_characters_xd():
    # Query params
    # Name
    # Part
    # Country
    # is_hamon_user
    # is_stand_user
    # is_gyro_user
    # living
    # is_human
    try:
        if not len(request.args):
            raise ValueError('Query witout params')
        params = validate_params(request.args)
        q = query_characters(params)
    except Exception as e:
        return jsonify({
            'message': f'<Invalid Query>',
            'error': e.args[0]

            }), HTTP_404_NOT_FOUND
    else:
        return jsonify({
            'params': params,
            'q': [ list_character_basic(x) for x in q ]
            }), HTTP_200_OK