from src.utils.database import Country
from validators import url

# <-- Country validators -->

def validate_country(item):
    # Es alfabetico (Code or name)
    if isinstance(item, str):
        if len(item) == 2:
            country = Country.query.filter_by(
                    country_code = item.upper()
                ).first()
            if not country:
                return country, 'Invalid code country'
        else:
            country = Country.query.filter_by(
                    country_name = item.upper()
                ).first()
            if not country:
                return country, 'Invalid name country'
    # Es numerico (Id)
    elif isinstance(item, int):
        country = Country.query.filter_by(
                id = item
            ).first()
        if not country:
            return country, 'Invalid ID country'
    # Invalid Country 
    else:
        return False, 'Invalid country'

    return country, 'Country is validate'

# <-- Images validators -->

def validate_images(item):
    # check this is exist the full body image 
    if item.get('full_body', None):
        if not url(item.get('full_body', '')):
            return False, 'Invalid "full_body" url'

    # check this is exist the full half image 
    if item.get('half_body', None):
        if not url(item.get('half_body', '')):
            return False, 'Invalid "half_body" url'
    return item, 'Urls validate'