from flask import Blueprint, jsonify, request
from src.utils.database import db, Stand, Stats, Image, Part
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from src.logic.custom_validators import validate_stand

from src.logic.list_content import list_images, list_pagination, list_stand
from src.constants.default_values import (
    INITIAL_PAGE,
    DEFAULT_CHARACTERS_PER_PAGE,
    MIN_CHARACTERS_PER_PAGE,
    MAX_CHARACTERS_PER_PAGE
)
stands = Blueprint('stands', __name__, url_prefix = '/api/v1/stands')

@stands.get('')
def get_stands():
    try:
        page = request.args.get('page', INITIAL_PAGE, type=int)
        per_page = request.args.get('per_page', DEFAULT_CHARACTERS_PER_PAGE, type=int)
        if not (per_page in range(MIN_CHARACTERS_PER_PAGE, MAX_CHARACTERS_PER_PAGE)):
            raise ValueError('Per Page is out of limit range')
        characters_data = Stand.query.paginate(page = page, per_page = per_page)
        data = list()

        for item in characters_data:
            data.append({
                'id': item.id,
                'name': item.name,
                'images': list_images(item.images_r) if item.images_r else None,
            })

        return jsonify({
            'message': 'hola',
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

        name = body.get('name', None)
        japanese_name = body.get('japanese_name', None)
        parts = body.get('parts', None)
        abilities = body.get('abilities', None)

        # Validate Stats, if incorrect data, create raise Value Error 

        stats = body.get('stats', None)
        new_stats = Stats(
            power = stats.get('power').upper(),
            speed = stats.get('speed').upper(),
            range = stats.get('range').upper(),
            durability = stats.get('durability').upper(),
            precision = stats.get('precision').upper(),
            potential = stats.get('potential').upper()
        )
        # Add Character in database
        db.session.add(new_stats)
        db.session.commit()

        # Other data 
        alther_name = body.get('alther_name', None)
        battlecry = body.get('battlecry', None)

        new_stand = Stand(
            name = name,
            japanese_name = japanese_name,
            alther_name = alther_name,
            abilities = abilities,
            battlecry = battlecry
        )

        # Validate images
        new_images = Image()
        if body.get('images', None):
            images = body.get('images')
            new_images = Image(full_body = images.get('full_body', None),
                               half_body = images.get('half_body', None))
            db.session.add(new_images)
            db.session.commit()

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
