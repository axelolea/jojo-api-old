# List Content Parts 

def list_image(item):
    return {
        'half_body': item.half_body,
        'full_body': item.full_body
    }


def list_part(item):
    return {
        'id': item.id,
        'name': item.name,
        'number': item.number,
        'japanese_name': item.japanese_name,
        'romanization_name': item.romanization_name,
        'alther_name': item.alther_name
    }

def list_characters(item):
    return {
        'id': item.id,
        'name': item.name,
        'alther_name': item.alther_name,
        'japanese_name': item.japanese_name,
        'catchphrase': item.catchphrase,
        'is_hamon_user': item.is_hamon_user,
        'is_stand_user': item.is_stand_user,
        'is_gyro_user': item.is_gyro_user,
        'living': item.living,
        'is_human': item.is_human,
        'country': list_country(item.user_country) if item.country_id else None,
        'images': list_image(item.user_images) if item.images_id else None,
    }


def list_country(item):
    return {
        'id': item.id,
        'country_name': item.country_name,
        'country_code': item.country_code
    }