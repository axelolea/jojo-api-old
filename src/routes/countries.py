from flask import Blueprint, jsonify, request
from src.utils.database import db, Country
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from src.logic.list_content import list_country
from src.constants.default_values import get_response

from schema import SchemaError

countries = Blueprint('countries', __name__, url_prefix = '/api/v1/countries')

from src.logic.custom_validators import country_validator

@countries.get('')
def get_country():
    countries_data = Country.query.all()
    countries_list = list()
    for item in countries_data:
        countries_list.append(list_country(item))
    return jsonify({
        'data': countries_list
        }), HTTP_200_OK


@countries.post('')
def post_country():
    try:
        body = country_validator(request.json)
        # Get params in body 
        if Country.query.filter_by(
            country_name = body.get('name')
        ).first() is not None:
            raise ValueError('La nacionalidad ya fue creada')
        if Country.query.filter_by(
            country_code = body.get('code')
        ).first() is not None:
            raise ValueError('La nacionalidad ya fue creada')
        # Create country obj 
        country = Country(
            country_name = body.get('name'),
            country_code = body.get('code')
        )
        # Add obj Coutry in database 
        db.session.add(country)
        db.session.commit()
    except SchemaError as e:
        return get_response(HTTP_400_BAD_REQUEST, e = e)
    except ValueError as e:
        return get_response(
            HTTP_400_BAD_REQUEST
        )
    # Return data 
    else:
        return get_response(
            HTTP_201_CREATED,
            data = list_country(country)
        )
