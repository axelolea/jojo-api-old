from flask import Blueprint, request
from src.utils.database import Image, db
from src.constants.http_status_codes import (
    HTTP_200_OK, 
    HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)
from src.logic.list_content import list_images

from src.constants.default_values import get_response


images = Blueprint('images', __name__, url_prefix = '/api/v1/images')


from random import choice

@images.get('/<int:id>')
def get_images_id(id):
    image = Image.query.get(id)
    if not image:
        return get_response(
            HTTP_404_NOT_FOUND,
            msg = f'Not found part with <id:{id}>'
        )
    return get_response(
        HTTP_200_OK ,
        data = list_images(image)
    )

@images.get('/random')
def get_random_image():
    image = choice(Image.query.all())
    return get_response(
        HTTP_200_OK,
        data = list_images(image)
    )


@images.get('/random/stand')
def get_random_image_stand():
    images = Image.query.filter(Image.type_image == 'STAND')
    image = choice(images.all())
    return get_response(
        HTTP_200_OK,
        data = list_images(image)
    )

@images.get('/random/character')
def get_random_image_character():
    images = Image.query.filter(Image.type_image == 'CHARACTER')
    image = choice(images.all())
    return get_response(
        HTTP_200_OK,
        data = list_images(image)
    )

# <-- Code Update images -->

from src.logic.custom_validators import validate_images


@images.put('/<int:id>')
def update_images_id(id):
    try:
        body = validate_images(request.json)
        image = Image.query.get(id)
        if not image:
            return get_response(
                HTTP_400_BAD_REQUEST,
                msg = f'Not found part with <id:{id}>'
            )
        if body.get('full_body') and image.full_body != body.get('full_body'):
            image.full_body = body.get('full_body')
        if body.get('half_body') and image.half_body != body.get('half_body'):
            image.half_body = body.get('half_body')
        db.session.commit()
    except:
        return get_response(HTTP_400_BAD_REQUEST)
    else:
        return get_response(
            HTTP_201_CREATED ,
            data = list_images(image)
        )