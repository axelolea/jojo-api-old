from flask import Blueprint, jsonify, request
from src.utils.database import db, Character, Image, Part
from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR)
from src.logic.list_content import list_characters, list_images, list_pagination
from src.constants.default_values import (
    INITIAL_PAGE,
    DEFAULT_CHARACTERS_PER_PAGE,
    MIN_CHARACTERS_PER_PAGE, 
    MAX_CHARACTERS_PER_PAGE,
    PARTS_IN_JOJOS)
from src.logic.custom_validators import validate_country, validate_images

# Create Blueprint 
characters = Blueprint('characters', __name__, url_prefix = '/api/v1/characters')


@characters.get('')
def get_characters():

    page = request.args.get('page', INITIAL_PAGE, type=int)
    per_page = request.args.get('per_page', DEFAULT_CHARACTERS_PER_PAGE, type=int)
    print(page, per_page)
    characters_data = Character.query.paginate(page = page, per_page = per_page)
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


@characters.get('/<int:id>')
def get_character_id(id):
    character = Character.query.filter_by(id = id).first()
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
    # +---------------+----------+----------+-----------------------------------------------
    # | Params        | Type     | Required | Description
    # +---------------+----------+----------+-----------------------------------------------
    # | name          | str      | True     | Alphanumeric name
    # | alther_name   | str      | False    | Alther name (for CR Claim. etc)
    # | japanese_name | str      | True     | Name in katakana or kanji
    # | parts         | list     | True     | List part aparization
    # | living        | bool     | True     | Is actual living character, skip reset universe of Pucchi
    # | catchphrase   | str      | False    | Frecuency Use Slogan 
    # | is_human      | bool     | False    | Is human character 
    # | country_id    | int/str  | False    | Response a section with id country or code
    # | images        | dict/obj | False    | Response with dictionary with contain a 2 min images
    # +---------------|----------|----------|------------------------------------------------|
    #           {
    #               "half_body" url with image [str] [null]
    #               "full_body" url with image [str] [null]
    #           }

    try:
        # Body with data params 
        body = request.json

        # Required params 

        name = body.get('name', None)
        japanese_name = body.get('japanese_name', None)
        parts = body.get('parts', None)

        # Clean list parts 

        # <-- Validators -->
        # Extremely required name and japanese version 

        if not (name and japanese_name):
            raise ValueError('El nombre, original y kanji no existen')
        if not parts:
            raise ValueError('Las partes de aparicion no existen')
        # Required parts in aparication
        if not (isinstance(parts, list)):
            raise ValueError('Las partes deben estar listadas')

        # ToDO validad parts is iterable
        parts = [ i for i in parts if (type(i) is int and i in range(1, PARTS_IN_JOJOS + 1))]
        print(parts)
        if not (all(parts) and len(parts) > 0):
            raise ValueError('Los valores en la lista son incorrectos')

        # Get Country 
        country = body.get('country', None)

        # Validar nacionalidad
        if country:
            country, msg = validate_country(country)
            if not country:
                raise ValueError(msg)

        # Get params with create character

        images = body.get('images', None)

        # Validate images 
        if images:
            images, msg = validate_images(images)
            if not images:
                raise ValueError(msg)
            else:
                images = Image(full_body = images.get('full_body'), half_body = images.get('half_body'))
                db.session.add(images)
                db.session.commit()

        # Set values or default values

        is_hamon_user = body.get('is_hamon_user', False)
        is_stand_user = body.get('is_stand_user', False)
        is_gyro_user = body.get('is_gyro_user', False)
        is_human = body.get('is_human', True)
        living = body.get('living', True)

        if not isinstance(is_hamon_user, bool):
            raise ValueError('Param "is_hamon_user" not boolean value')
        if not isinstance(is_gyro_user, bool):
            raise ValueError('Param "is_gyro_user" not boolean value')
        if not isinstance(is_stand_user, bool):
            raise ValueError('Param "is_stand_user" not boolean value')
        if not isinstance(is_human, bool):
            raise ValueError('Param "is_human" not boolean value')
        if not isinstance(living, bool):
            raise ValueError('Param "living" not boolean value')


        # Set values or Null 
        alther_name = body.get('alther_name', None)
        catchphrase = body.get('catchphrase', None)

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

        if country:
            character.country_id = country.id
        if images.id:
            character.images_id = images.id
        # Append character with parts 
        for number in parts:
            part = Part.query.filter_by(number = number).first()
            character.parts_r.append(part)

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
        "error": 'Uno de los parametros es incorrecto',
        }), HTTP_400_BAD_REQUEST
    # except:
    #     return jsonify({
    #     'status': 500,
    #     'type': 'ServerError',
    #     "error": 'Problemas internos D:',
    #     }), HTTP_500_INTERNAL_SERVER_ERROR
    # <-- Send data of character created and status 201 [Created] -->
    else:
        return jsonify({
            'status': 201,
            'message': f'Character: {character.name} is created successfully',
            'data': list_characters(character)
            }), HTTP_201_CREATED