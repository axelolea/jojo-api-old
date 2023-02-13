from schema import Schema, Optional, Or, And, Regex, Use
from src.constants.default_values import (
    STATS_VALUES,
    PARTS_IN_JOJOS,
    URL_REGEX,
    INITIAL_PAGE,
    DEFAULT_PER_PAGE,
    MIN_PER_PAGE,
    MAX_PER_PAGE
)

def string_to_bool(value):
    if value.lower() in ('yes', 'true', 'y', '1'):
        return True
    if value.lower() in ('no', 'false', 'f', '0'):
        return False
    return None


images_schema = Schema({
    'half_body': And(str, Regex(URL_REGEX)),
    Optional('full_body'): And(str, Regex(URL_REGEX)),
})


stats_schema = Schema({
    'power': And(
        str, Use(str.upper),
        lambda x: x in STATS_VALUES
    ),
    'speed': And(
        str, Use(str.upper),
        lambda x: x in STATS_VALUES
    ),
    'range': And(
        str, Use(str.upper),
        lambda x: x in STATS_VALUES
    ),
    'durability': And(
        str, Use(str.upper),
        lambda x: x in STATS_VALUES
    ),
    'precision': And(
        str, Use(str.upper),
        lambda x: x in STATS_VALUES
    ),
    'potential': And(
        str, Use(str.upper),
        lambda x: x in STATS_VALUES
    )
})


def validate_character(data):
    character_schema = Schema({
        'name': And(str, lambda x : 0 < len(x) <= 100),
        'japanese_name': And(str, lambda x : 0 < len(x) <= 100),
        'parts': [And(int, lambda x : 0 < x <= PARTS_IN_JOJOS)],
        Optional('alther_name'): And(str, lambda x : 0 < len(x) <= 100),
        Optional('catchphrase'): And(str, lambda x : 0 < len(x) <= 200),
        Optional('is_stand_user', default = False): bool,
        Optional('is_hamon_user', default = False): bool,
        Optional('is_gyro_user', default = False): bool,
        Optional('living', default = True): bool,
        Optional('is_human', default = True): bool,
        Optional('country'): Or(And(str, lambda x : len(x) == 2), int),
        Optional('images'): images_schema,
        Optional('stands'): [int, str],
    })
    # ToDo Create conditional
    # If 'is_stand_user' is True
    # 'stands' is need required
    return character_schema.validate(data)

def validate_stand(data):
    stand_schema = Schema({
        'name': And(str, lambda x : 0 < len(x) <= 100),
        'japanese_name': And(str, lambda x : 0 < len(x) <= 100),
        'abilities': str,
        'stats': stats_schema,
        'parts': [And(int, lambda x : 0 < x <= PARTS_IN_JOJOS)],
        Optional('alther_name'): And(str, lambda x : 0 < len(x) <= 100),
        Optional('battlecry'): And(str, lambda x : 0 < len(x) <= 120),
        Optional('images'): images_schema,
    })
    return stand_schema.validate(data)

def validate_character_params(params):
    params_schema = Schema({
        Optional('name'): str,
        Optional('parts'): And(
            Use(
                lambda x : [
                    i for i in x.split(',') if i.isdigit()
                ]
            ),
            list,
            len
        ),
        Optional('country'): Or(
            And(str, lambda x : len(x) == 2),
            And(str, lambda x : x.isdigit())
        ),
        Optional(Or(
                'is_hamon_user',
                'is_stand_user',
                'is_gyro_user',
                'living',
                'is_human'
            )
        ): And(
            Use(string_to_bool),
            bool
        ),
    })
    return params_schema.validate(dict(params))

def validate_stand_params(params):
    params_scheman = Schema({
        Optional('name'): And(
            str,
            lambda x : len(x) <= 100
        ),
        Optional('parts'): And(
            Use(
                lambda x : [
                    i for i in x.split(',') if i.isdigit()
                ]
            ),list,len),
        Optional('battlecry'): And(str,lambda x : len(x) <= 100),
        Optional('abilities'): And(str,lambda x : len(x) <= 100),
        Optional(Or(
            'power',
            'speed',
            'range',
            'durability',
            'precision',
            'potential')
        ): And(
            str,
            Use(str.upper),
            lambda x : x in STATS_VALUES
        )
    })
    return params_scheman.validate(dict(params))

def validate_pagination(params):
   params_schema = Schema({
        Optional('page', default = INITIAL_PAGE): Use(int),
        Optional('per_page', default = DEFAULT_PER_PAGE): And(
            Use(int),
            lambda x : MIN_PER_PAGE <= x <= MAX_PER_PAGE
        ),
   })
   return params_schema.validate(dict(params))

def validate_images(data):
    images_update_schema = Schema({
        Optional(Or(
            'half_body',
            'full_body'
        )): And(str, Regex(URL_REGEX)),
    })
    return images_update_schema.validate(dict(data))

def country_validator(data):
    country_schema = Schema({
        'name': And(
            Use(str.upper),
            lambda x : len(x) <= 50
        ),
        'code': And(
            Use(str.upper),
            lambda x: len(x) == 2 and x.isalpha())
    })
    return country_schema.validate(dict(data))

def part_validator(data):
    part_schema = Schema({
        'name': And(
            str,
            lambda x : len(x) <= 100
        ),
        'number': And(
            int
        ),
        'japanese_name': And(
            str,
            lambda x : len(x) <= 100
        ),
        'romanization_name': And(
            str,
            lambda x : len(x) <= 100
        ),
        Optional('alther_name'): And(
            str,
            lambda x : len(x) <= 100
        ),
    })
    return part_schema.validate(dict(data))