from validator import validate, rules as R
from src.logic.custom_rules import *
from schema import Schema, Optional, Or, And, Regex, Use
from src.constants.default_values import PARTS_IN_JOJOS, URL_REGEX
from src.constants.default_values import STATS_NAMES, STATS_VALUES



def string_to_bool(value):
  if value.lower() in ('yes', 'true', 'y', '1', 'no', 'false', 'f', '0'):
     return True
  return False

images_schema = Schema({
    Optional('full_body'): And(str, Regex(URL_REGEX)),
    'half_body': And(str, Regex(URL_REGEX))
})

stats_schema = Schema({
    'power': And(str, Use(str.upper), lambda x: x in STATS_VALUES),
    'speed': And(str, Use(str.upper), lambda x: x in STATS_VALUES),
    'range': And(str, Use(str.upper), lambda x: x in STATS_VALUES),
    'durability': And(str, Use(str.upper), lambda x: x in STATS_VALUES),
    'precision': And(str, Use(str.upper), lambda x: x in STATS_VALUES),
    'potential': And(str, Use(str.upper), lambda x: x in STATS_VALUES)
})


def validate_character(data):
    character_schema = Schema({
        'name': And(str, lambda x : 0 < len(x) <= 100),
        'japanese_name': And(str, lambda x : 0 < len(x) <= 100),
        Optional('alther_name'): And(str, lambda x : 0 < len(x) <= 100),
        Optional('catchphrase'): And(str, lambda x : 0 < len(x) <= 200),
        Optional('is_stand_user', default = False): bool,
        Optional('is_hamon_user', default = False): bool,
        Optional('is_gyro_user', default = False): bool,
        Optional('living', default = True): bool,
        Optional('is_human', default = True): bool,
        Optional('country'): Or(And(str, lambda x : len(x) == 2), int),
        Optional('images'): images_schema,
        'parts': [And(int, lambda x : 0 < x <= PARTS_IN_JOJOS)],
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
        Optional('alther_name'): And(str, lambda x : 0 < len(x) <= 100),
        'abilities': str,
        Optional('battlecry'): And(str, lambda x : 0 < len(x) <= 120),
        'stats': stats_schema,
        Optional('images'): images_schema,
        'parts': [And(int, lambda x : 0 < x <= PARTS_IN_JOJOS)]
    })
    return stand_schema.validate(data)

def validate_character_params(params):
    schema = Schema({
        Optional('name'): str,
        Optional('parts'): str,
        Optional('country'): Or(And(str, lambda x : len(x) == 2), And(str, lambda x : x.isdigit())),
        Optional('is_hamon_user'): And(str, string_to_bool),
        Optional('is_stand_user'): And(str, string_to_bool),
        Optional('is_gyro_user'): And(str, string_to_bool),
        Optional('living'): And(str, string_to_bool),
        Optional('is_human'): And(str, string_to_bool)
    })
    return schema.validate(dict(params))
