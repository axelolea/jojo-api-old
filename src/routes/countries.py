from flask import Blueprint, jsonify, request
from src.utils.database import db
from src.models.Countries import Country
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from src.logic.list_content import list_country

countries = Blueprint('countries', __name__, url_prefix = '/api/v1/countries')


@countries.get('/')
def get_parts():

    return jsonify({
        'data': 'parts_list'
        }), HTTP_200_OK


@countries.post('/')
def post_country():
    params = request.args.get('nmms', None)
    name = request.json.get('name', None)
    code = request.json.get('code', None)
    print(params)
    if not (name and code):
        return jsonify({
        'message': 'Faltan parametros'
        }), HTTP_400_BAD_REQUEST
    if not len(code) == 2:
        return jsonify({
        'message': 'Codigo no valido'
        }), HTTP_400_BAD_REQUEST
    if Country.query.filter_by(country_name = name).first() is not None:
        return jsonify({
        'message': 'La nacionalidad ya fue creada'
        }), HTTP_400_BAD_REQUEST
    if Country.query.filter_by(country_code = code).first() is not None:
        return jsonify({
        'message': 'La nacionalidad ya fue creada'
        }), HTTP_400_BAD_REQUEST
    country = Country(country_name = name, country_code = code)
    db.session.add(country)
    db.session.commit()
    return jsonify({
        'data': list_country(country)
        }), HTTP_201_CREATED