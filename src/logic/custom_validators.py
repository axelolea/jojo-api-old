from validator import validate, rules as R
from src.logic.custom_rules import *

def validate_character(data):
    rules_character = {
        "name":             [ R.Required(), R.String(), R.Max(100) ],
        "alther_name":      [ CustomString(100) ],
        "japanese_name":    [ R.Required(), R.String(), R.Max(100) ],
        "catchphrase":      [ CustomString(200) ],
        "is_stand_user":    [ R.Required(), Boolean() ],
        "is_hamon_user":    [ R.Required(), Boolean() ],
        "is_gyro_user":     [ R.Required(), Boolean() ],
        "living":           [ R.Required(), Boolean() ],
        "is_human":         [ R.Required(), Boolean() ],
        "country":          [ Country() ],
        "images":           [ Images() ],
        "parts":            [ Parts() ],
        "stands":           [ Stands( True if data.get('is_stand_user', None) else False ) ]
    }
    result, validate_data, errors = validate(data, rules_character, return_info=True)
    if not result:
        raise ValueError(errors)

    return validate_data

def validate_stand(data):
    rules_stand = {
        "name":         [ R.Required(), R.String(), R.Max(100) ],
        "japanese_name":[ R.Required(), R.String(), R.Max(100) ],
        "alther_name":  [ CustomString(100) ],
        "abilities":    [ R.Required(), R.String() ],
        "battlecry":    [ CustomString(120) ],
        "stats":        [ Stats() ],
        "images":       [ Images() ],
        "parts":        [ Parts() ],
    }
    result, validate_data, errors = validate(data, rules_stand, return_info=True)
    if not result:
        raise ValueError(errors)

    return validate_data
