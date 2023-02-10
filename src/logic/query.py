from src.utils.database import Character, Part, Country, Stand, Stats
from src.constants.default_values import STATS_NAMES

def query_characters(params):
    q = Character.query
    # is_hamon_user
    # is_stand_user
    # is_gyro_user
    # living
    # is_human
    if params.get('name'):
        q = q.filter(
            Character.name.like(f'%{params.get("name")}%') | 
            Character.alther_name.like(f'%{params.get("name")}%')
            )
    if params.get('parts'):
        q = q.filter(
            Character.parts_r.any(Part.number.in_(params.get('parts')))
            )
    if params.get('country'):
        q = q.filter(
            Character.country_r.has((
                Country.country_code == params.get('country')) | (
                Country.id == params.get('country'))
                )
            )
    
    if (type(params.get('is_hamon_user')) == bool):
        q = q.filter(
            Character.is_hamon_user == params.get('is_hamon_user')
            )
    
    if (type(params.get('is_stand_user')) == bool):
        q = q.filter(
            Character.is_stand_user == params.get('is_stand_user')
            )

    if (type(params.get('is_gyro_user')) == bool):
        q = q.filter(
            Character.is_gyro_user == params.get('is_gyro_user')
            )

    if (type(params.get('living')) == bool):
        q = q.filter(
            Character.living == params.get('living')
            )

    if (type(params.get('is_human')) == bool):
        q = q.filter(
            Character.is_human == params.get('is_human')
            )

    return q.all()


def query_stands(params):
    q = Stand.query
    if params.get('name'):
        q = q.filter(
            Stand.name.like(f'%{params.get("name")}%') | 
            Stand.alther_name.like(f'%{params.get("name")}%')
            )
    if params.get('parts'):
        q = q.filter(
            Stand.parts_r.any(Part.number.in_(params.get('parts')))
            )
    if params.get('battlecry'):
        q = q.filter(
            Stand.battlecry.like(f'%{params.get("battlecry")}%')
            )
    if params.get('abilities'):
        q = q.filter(
            Stand.abilities.like(f'%{params.get("abilities")}%')
            )
    for name_stat in STATS_NAMES:
        if params.get(name_stat):
            q = q.filter(
                Stand.stats_r.has(
                    getattr(Stats, name_stat).like(params.get(name_stat))
                )
            )
    return q.all()