from flask import Blueprint, jsonify, request
from src.utils.database import db, Character, Country, Image
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from validators import url

from src.logic.list_content import list_characters

from src.constants.default_params import INITIAL_PAGE, DEFAULT_CHARACTERS_PER_PAGE, MIN_CHARACTERS_PER_PAGE, MAX_CHARACTERS_PER_PAGE

characters = Blueprint('characters', __name__, url_prefix = '/api/v1/characters')


@characters.get('/')
def get_characters():

    page = request.args.get('page', INITIAL_PAGE, type=int)
    per_page = request.args.get('page', DEFAULT_CHARACTERS_PER_PAGE, type=int)

    characters_data = Character.query.all.paginate(page = page, per_page = per_page)

    data = list()

    return jsonify({
        'message': 'hola'
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


@characters.post('/')
def post_character():
    # Params:
    # name -> Alphanumeric name [Required][str]
    # alther_name -> Alther name (for CR Claim. etc) [Null][str]
    # japanese_name -> Name in katakana or kanji [required][str]
    # catchphrase -> Frecuency Use Slogan [Null][str]
    # living -> Is actual living character, skip reset universe of Pucchi [requiered][bool]
    # is_human -> Is human character [bool][true]
    # country_id -> Response a section with id country or code [null][int or str(2)]
    # images -> response with dictionary with contain a 2 min images [dict][null]
    #           {
    #               "half_body" url with image [str] [null]
    #               "full_body" url with image [str] [null]
    #           }
    # parts -> list with numbers the part aparition [list][required]

    # Body with data params 
    body = request.json

    # Required params 

    name = body.get('name', None)
    japanese_name = body.get('japanese_name', None)
    parts = body.get('parts', None)
    # Clean list parts 
    parts = [ i for i in parts if (type(i) is int and i in range(0, 9))]
    # Validators 

    # Extremely required name and japanese version 
    if not (name and japanese_name):
        return jsonify({
        'message': 'Faltan nombres del personajes, son requeridos el nombre y su version en katakana o kanji'
        }), HTTP_400_BAD_REQUEST
    # Required parts in aparication 
    if not parts:
        return jsonify({
        'message': 'Falta lista con las partes de aparicion'
        }), HTTP_400_BAD_REQUEST
    elif not (isinstance(parts, list) and all(parts)):
        return jsonify({
        'message': 'Las partes deben estar listadas'
        }), HTTP_400_BAD_REQUEST

    country = body.get('country', None)

    # Validar nacionalidad
    if body.get('country'):
        # Es alfabetico (Code or name)
        if isinstance(body.get('country'), str):
            if len(body.get('country')) == 2:
                country = Country.query.filter_by(
                        country_code = body.get('country').upper()
                    ).first()
                if not country:
                    return jsonify({
                    'message': 'Invalid code country'
                    }), HTTP_400_BAD_REQUEST
            else:
                country = Country.query.filter_by(
                        country_name = body.get('country').upper()
                    ).first()
                if not country:
                    return jsonify({
                    'message': 'Invalid name country'
                    }), HTTP_400_BAD_REQUEST
        # Es numerico (Id)
        elif isinstance(body.get('country'), int):
            country = Country.query.filter_by(
                    id = body.get('country')
                ).first()
            if not country:
                return jsonify({
                'message': 'Invalid ID country'
                }), HTTP_400_BAD_REQUEST
        # Invalid Country 
        else:
            return jsonify({
                'message': 'Invalid country'
                }), HTTP_400_BAD_REQUEST

    # Get params with create character

    images = body.get('images', None)
    flag = False
    if images:
        img = Image()
        if not url(images.get('half_body', '')):
            return jsonify({
                'message': 'Invalid < half_body > url'
                }), HTTP_400_BAD_REQUEST
        else:
            flag = True
            img.half_body = images.get('half_body')
        if not url(images.get('full_body', '')):
            return jsonify({
                'message': 'Invalid "full_body" url'
                }), HTTP_400_BAD_REQUEST
        else:
            flag = True
            img.full_body = images.get('full_body')


    # Set values or default 

    is_hamon_user = body.get('is_hamon_user', False)
    is_stand_user = body.get('is_stand_user', False)
    is_gyro_user = body.get('is_gyro_user', False)
    is_human = body.get('is_human', True)
    living = body.get('living', True)

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
    if flag:
        db.session.add(img)
        db.session.commit()
        character.images_id = img.id
    # Add obj Coutry in database 
    db.session.add(character)
    db.session.commit()

    return jsonify({
        'message': f'Character: {character.name} is created successfully',
        'data': list_characters(character)
        }), HTTP_201_CREATED