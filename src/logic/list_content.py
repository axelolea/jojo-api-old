# List Content Parts 

def list_image(item):
    return {
        'half_body': item.half_body,
        'full_body': item.full_body
    }


def list_parts(item):
    return {

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
        'country': list_country(item.country_r) if item.country_r else None,
        'images': list_image(item.images_r) if item.images_r else None,
        'parts': [ i.number for i in item.parts_r]
    }


def list_country(item):
    return {
        'country_id': item.id,
        'country_name': item.country_name,
        'country_code': item.country_code
    }