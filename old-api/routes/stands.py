from flask import Blueprint, jsonify, request
from app.utils.database import (
    db,
    Stand, 
    Stats, 
    Image, 
    Part
)

from app.constants.default_values import (
    get_response
)

from app.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)

from app.logic.custom_validators import (
    validate_stand,
    validate_pagination,
    validate_stand_params
)

from app.logic.list_content import (
    list_images,
    list_pagination,
    list_stand,
    list_stand_basic
)

from schema import (
    SchemaError, 
    SchemaMissingKeyError, 
    SchemaWrongKeyError
)

from app.logic.query import query_stands

stands = Blueprint('stands', __name__, url_prefix = '/api/v1/stands')

@stands.get('')
def get_stands():
    try:
        params = validate_pagination(request.args)
        characters_data = Stand.query.paginate(
            page = params.get('page'),
            per_page = params.get('per_page')
        )
        data = list()

        for item in characters_data:
            data.append(list_stand_basic(item))
    except ValueError as e:
        return jsonify({
            'status': 400,
            'type': type(e).__name__,
            'message': e.args[0],
            "error": 'Uno de los parametros es incorrecto',
            }), HTTP_400_BAD_REQUEST
    else:
        return get_response(
            HTTP_200_OK,
            data = data,
            pagination = list_pagination(characters_data)
            )
        return jsonify({
                    'data': data,
                    'pagination': list_pagination(characters_data)
                    }), HTTP_200_OK


@stands.get('/<int:id>')
def get_character_id(id):
    stand = Stand.query.get(id)
    if not stand:
        return jsonify({
            'message': f'Not found part with <id:{id}>'
            }), HTTP_404_NOT_FOUND
    return jsonify({
        'data': list_stand(stand)
        }), HTTP_200_OK


@stands.post('')
def post_stands():
    # <-- Params will created a character -->
    # +---------------+----------+----------+---------------------------------+
    # | Params        | Type     | Required | Description                     |
    # +---------------+----------+----------+---------------------------------+
    # | name          | str      | True     | Alphanumeric name.              |
    # | japanese_name | str      | True     | Name in katakana or kanji.      |
    # | alther_name   | str      | False    | Alther name (for CR Claim. etc).|
    # | parts         | list     | True     | List part aparization.          |
    # | abilities     | bool     | True     | String with all abilities       |
    # | battlecry     | str      | False    | Frecuency cry in figth.         |
    # | stats         | dict/obj | True     | Obj with stand stats.           |
    # | images        | dict/obj | False    | Dictionary with contain two.    |
    # |               |          |          | min images urls.                |
    # +---------------|----------|----------|---------------------------------+
    #
    # <-- Dictionaries -->
    #
    # images:
    #           {
    #               "half_body"     url image [str] [null]
    #               "full_body"     url image [str] [null]
    #           }
    #
    # stats:
    #           {
    #               "power"         Value in static list str(8)
    #               "speed"         Value in static list str(8)
    #               "range"         Value in static list str(8)
    #               "durability"    Value in static list str(8)
    #               "precision"     Value in static list str(8)
    #               "potential"     Value in static list str(8)
    #           }
    #
    # from src.constants.default_values import STATS_VALUES
    # 
    # STATS_VALUES = [None, "A", "B", "C", "D", "E", "INFINITE", "?"]
    try:
        body = validate_stand(request.json)

        # Validate Stats, if incorrect data, create raise Value Error 

        stats = body.get('stats')
        new_stats = Stats(
            power = stats.get('power'),
            speed = stats.get('speed'),
            range = stats.get('range'),
            durability = stats.get('durability'),
            precision = stats.get('precision'),
            potential = stats.get('potential')
        )
        # Add Character in database
        db.session.add(new_stats)
        db.session.commit()

        new_stand = Stand(
            name = body.get('name'),
            japanese_name = body.get('japanese_name'),
            alther_name = body.get('alther_name'),
            abilities = body.get('abilities'),
            battlecry = body.get('battlecry')
        )

        # Validate images
        new_images = Image()
        if body.get('images'):
            images = body.get('images')
            new_images = Image(
                full_body = images.get('full_body'),
                half_body = images.get('half_body'),
                type_image = 'STAND'
            )
            db.session.add(new_images)
            db.session.commit()

        parts = body.get('parts')
        
        if new_images.id:
            new_stand.images_id = new_images.id
        if new_stats.id:
            new_stand.stats_id = new_stats.id
        for number in parts:
            part = Part.query.filter_by(number = number).first()
            new_stand.parts_r.append(part)
        # Add Character in database
        db.session.add(new_stand)
        db.session.commit()
    except ValueError as e:
        return jsonify({
        'status': 400,
        'type': type(e).__name__,
        'message': e.args[0],
        'error': 'One or more arguments are invalid',
        }), HTTP_400_BAD_REQUEST
    else:
        return jsonify({
            'data': list_stand(new_stand)
        }), HTTP_201_CREATED


@stands.get('/query')
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
        params = validate_stand_params(request.args)
        if not len(request.args):
            raise ValueError('Query witout params')
        q = query_stands(params)
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
            'q': [ list_stand_basic(x) for x in q ]
            }), HTTP_200_OK