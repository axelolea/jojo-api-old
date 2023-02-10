from flask import jsonify

INITIAL_PAGE = 1
DEFAULT_PER_PAGE = 10
MIN_PER_PAGE = 5
MAX_PER_PAGE = 50
PARTS_IN_JOJOS = 8
URL_REGEX = r'(?:https?:\/\/)?(?:[^?\/\s]+[?\/])(.*)'
STATS_VALUES = ('NULL', 'A', 'B', 'C', 'D', 'E', 'INFINITE', '?')
STATS_NAMES = ('power','speed','range','durability','precision','potential')

def get_response(code, **args):

    data = args.get('data')
    e = args.get('e')
    pagination = args.get('pagination')
    
    response = {
        'status': code,
    }

    if data:
        response['data'] = data,
    if pagination:
        response['message'] = pagination,
    if args.get('msg'):
        response['message'] = args.get('msg'),
    if e:
        response['type'] = type(e).__name__
        response['error'] = e.args[0]

    return jsonify(response), code