# List Content Parts 

def list_images(item):
    return {
        'id': item.id,
        'half_body': item.half_body,
        'full_body': item.full_body,
    }


def list_part(item):
    return {
        'name': item.name,
        'number': item.number,
        'japanese_name': item.japanese_name,
        'romanization_name': item.romanization_name,
        'alther_name': item.alther_name
    }

def list_stats(item):
    return {
        'power': item.power,
        'speed': item.speed,
        'range': item.range,
        'durability': item.durability,
        'precision': item.precision,
        'potential': item.potential
    }


def list_character_basic(item):
    return {
        'id': item.id,
        'name': item.name,
        'japanese_name': item.japanese_name,
        'images': list_images(item.images_r) if item.images_r else None,
    }


def list_stand_basic(item):
    return {
        'id': item.id,
        'name': item.name,
        'japanese_name': item.japanese_name,
        'images_id': list_images(item.images_r) if item.images_r else None,
    }


def list_stand(item):
    return {
        'id': item.id,
        'name': item.name,
        'japanese_name': item.japanese_name,
        'alther_name': item.alther_name,
        'abilities': item.abilities,
        'battlecry': item.battlecry,
        'images_id': list_images(item.images_r) if item.images_r else None,
        'stats_id': list_stats(item.stats_r) if item.stats_r else None,
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
        'images': list_images(item.images_r) if item.images_r else None,
        'parts': [ i.number for i in item.parts_r],
        'stands': [{ 'id': x.id, 'name': x.name } for x in item.stands_r] if item.stands_r else None
    }


def list_country(item):
    return {
        'id': item.id,
        'country_name': item.country_name,
        'country_code': item.country_code
    }

def list_pagination(item):
    return {
        'page': item.page,
        'pages': item.pages,
        'total_count': item.total,
        'prev': item.prev_num,
        'next': item.next_num,
        'has_prev': item.has_prev,
        'has_next': item.has_next,
        }