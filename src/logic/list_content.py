# List Content Parts 

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
        'japanese_name': item.japanese_name,
        'catchphrase': item.catchphrase,
        'is_stand_user': item.is_stand_user,
        'living': item.living,
        'is_human': item.is_human,
        'country_id': item.country_id,
        'images_id': item.images_id
    }


def list_country(item):
    return {
        'id': item.id,
        'country_name': item.country_name,
        'country_code': item.country_code
    }