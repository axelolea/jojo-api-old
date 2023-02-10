from flask import Blueprint
from src.utils.database import Image, db
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
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