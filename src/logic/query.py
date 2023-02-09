from src.utils.database import Character, Part, Country


def string_to_bool(value):
  if value.lower() in ("yes", "true", "y", "1"):
      return True
  elif value.lower() in ("no", "false", "f", "0"):
      return False
  return None


def query_characters(params):
    q = Character.query
    # is_hamon_user
    # is_stand_user
    # is_gyro_user
    # living
    # is_human
    if params.get('name', None):
        q = q.filter(
            Character.name.like(f'%{params.get("name")}%') | 
            Character.alther_name.like(f'%{params.get("name")}%')
            )
    if params.get('parts', None):
        parts_list = params.get('parts').split(',')
        q = q.filter(
            Character.parts_r.any(Part.number.in_(parts_list))
            )
    if params.get('country', None):
        q = q.filter(
            Character.country_r.has((
                Country.country_code == params.get('country')) | (
                Country.id == params.get('country', None)
                ))
            )
    if (params.get('is_hamon_user', None) and
        type(string_to_bool(params.get('is_hamon_user', None)))) == bool:
            value = string_to_bool(params.get('is_hamon_user', None))
            q = q.filter(
                Character.is_hamon_user == value
                )
    return q.all()