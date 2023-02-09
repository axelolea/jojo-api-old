

INITIAL_PAGE = 1
DEFAULT_CHARACTERS_PER_PAGE = 15
MIN_CHARACTERS_PER_PAGE = 5
MAX_CHARACTERS_PER_PAGE = 50
PARTS_IN_JOJOS = 8
URL_REGEX = r'(?:https?:\/\/)?(?:[^?\/\s]+[?\/])(.*)'
STATS_VALUES = ('Null', 'A', 'B', 'C', 'D', 'E', 'INFINITE', '?')
STATS_NAMES = ('power','speed','range','durability','precision','potential')

def get_error_response(e, code, msg):
    return {
        'status': code,
        'type': type(e).__name__,
        'error': e.args[0],
        'message': msg,
    }, code