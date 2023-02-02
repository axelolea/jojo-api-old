from flask import Blueprint, jsonify, request
from src.utils.database import db, Country
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from src.logic.list_content import list_country

countries = Blueprint('countries', __name__, url_prefix = '/api/v1/countries')


@countries.get('/')
def get_parts():
    countries_data = Country.query.all()
    countries_list = list()
    for item in countries_data:
        countries_list.append(list_country(item))
    return jsonify({
        'data': countries_list
        }), HTTP_200_OK


@countries.post('/')
def post_country():

    # Get params in body 
    name = request.json.get('name', None)
    code = request.json.get('code', None)
    # Valid content data in params 
    if not (name and code):
        return jsonify({
        'message': 'Faltan parametros'
        }), HTTP_400_BAD_REQUEST
    # Valid syntax of Code
    if not (len(code) == 2 and code.isalpha()):
        return jsonify({
        'message': 'Codigo no valido, debe tener logitud de 2 y alfabetico'
        }), HTTP_400_BAD_REQUEST
    if Country.query.filter_by(country_name = name).first() is not None:
        return jsonify({
        'message': 'La nacionalidad ya fue creada'
        }), HTTP_400_BAD_REQUEST
    if Country.query.filter_by(country_code = code).first() is not None:
        return jsonify({
        'message': 'La nacionalidad ya fue creada'
        }), HTTP_400_BAD_REQUEST
    # Upper the code
    code = code.upper()
    # Create country obj 
    country = Country(country_name = name, country_code = code)
    # Add obj Coutry in database 
    db.session.add(country)
    db.session.commit()
    # Return data 
    return jsonify({
        'data': list_country(country)
        }), HTTP_201_CREATED