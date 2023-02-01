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