from flask import Blueprint, jsonify, request
from jojo.utils.database import (
    db,
    Character,
    Image,
    Part,
    Stand,
    Country
)
from jojo.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from jojo.logic.list_content import (
    list_characters,
    list_pagination,
    list_character_basic
)
from jojo.constants.default_values import (
    get_response
)

from jojo.logic.query import query_characters

from jojo.logic.custom_validators import (
    validate_character,
    validate_character_params,
    validate_pagination
)
# Create Blueprint 
characters = Blueprint('characters', __name__, url_prefix = '/api/v1/characters')

from schema import SchemaMissingKeyError, SchemaError, SchemaWrongKeyError


@characters.get('')
def get_characters():
    try:
        params = validate_pagination(request.args)
        characters_data = Character.query.paginate(
            page = params.get('page'),
            per_page = params.get('per_page'))

        data = list()

        for item in characters_data:
            data.append(list_character_basic(item))
    except SchemaError as e:
        return get_response(
            HTTP_400_BAD_REQUEST,
            msg = 'Invalid pagination params.',
            e = e
        )
    except ValueError as e:
        return jsonify({
            'status': 400,
            'type': type(e).__name__,
            'message': e.args[0],
            "error": 'Params are invalid.',
            }), HTTP_400_BAD_REQUEST
    else:
        return jsonify({
            'data': data,
            'pagination': list_pagination(characters_data)
            }), HTTP_200_OK


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
        is_hamon_user = body.get('is_hamon_user')
        is_stand_user = body.get('is_stand_user')
        is_gyro_user = body.get('is_gyro_user')
        is_human = body.get('is_human')
        living = body.get('living')
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
            new_images = Image(
                full_body = images.get('full_body'),
                half_body = images.get('half_body'),
                type_image = 'CHARACTER'
            )
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
        return get_response(
            HTTP_400_BAD_REQUEST,
            msg = 'Params are invalid.',
            e = e
            );
    except (SchemaError, SchemaMissingKeyError, SchemaWrongKeyError) as e:
        return get_response(
            HTTP_400_BAD_REQUEST,
            msg = 'Params are invalid.',
            e = e
            )
    # <-- General exception error return -->
    except:
        return get_response(
            HTTP_500_INTERNAL_SERVER_ERROR
            )
    # <-- Send data of character created and status 201 [Created] -->
    else:
        return jsonify({
            'status': 201,
            'message': f'Character: {character.name} is created successfully',
            'data': list_characters(character)
            }), HTTP_201_CREATED


@characters.get('/query')
def query():
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
        params = validate_character_params(request.args)
        if not len(request.args):
            raise ValueError('Query witout params')
        q = query_characters(params)
    except (SchemaError, SchemaMissingKeyError, SchemaWrongKeyError) as e:
        return get_response(
            HTTP_400_BAD_REQUEST,
            msg = 'Params are invalid.',
            e = e
        )
    except ValueError as e:
        return jsonify({
            'message': e.args[0],
            'error': type(e).__name__
            }), HTTP_404_NOT_FOUND
    else:
        return jsonify({
            'q': [ list_character_basic(x) for x in q ]
            }), HTTP_200_OK