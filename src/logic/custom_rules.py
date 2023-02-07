from validator.rules import Rule
from src.constants.default_values import PARTS_IN_JOJOS
from validators import url
from src.constants.default_values import STATS_NAMES, STATS_VALUES

class Boolean(Rule):
    def __init__(self):
        Rule.__init__(self)

    def check(self, arg):
        self.set_error(f'{arg} is not Boolean value')
        return type(arg) == bool

class CustomString(Rule):
    def __init__(self, max):
        Rule.__init__(self)
        self.max = max
    def check(self, arg):
        if arg == None:
            return True
        if type(arg) != str:
            self.set_error(f'{arg} is not String value')
            return False
        if len(arg) > self.max:
            self.set_error(f'{arg} are must max length 200 characters')
            return False 
        return True


class Country(Rule):
    def __init__(self):
        Rule.__init__(self)
    def check(self, arg):
        if arg == None:
            return True
        if type(arg) == str:
            if len(arg) == 2 and arg.isalpha():
                return True
        if type(arg) == int:
            if arg > 0:
                return True
        self.set_error(f'Country {arg} is not Code or ID')
        return False


class Stands(Rule):
    def __init__(self, isRequired):
        Rule.__init__(self)
        self.isRequired = isRequired
    def check(self, arg):
        if not self.isRequired:
            return True
        if not isinstance(arg, list):
            self.set_error(f'{arg} is not List')
            return False
        for item in arg:
            if type(item) == int:
                if item > 0:
                    continue
            elif type(item) == str:
                continue
            self.set_error(f'{item} is not valid stand')
            return False
        return True


class Parts(Rule):
    def __init__(self):
        Rule.__init__(self)
    def check(self, arg):
        if not isinstance(arg, list):
            self.set_error(f'{arg} is not list')
            return False
        if not len(arg) > 0:
            self.set_error(f'{arg} is not valid list')
            return False
        for item in arg:
            if (type(item) == int and item > 0):
                continue
            self.set_error(f'{item} is not valid ID')
            return False
        return True

class Images(Rule):
    def __init__(self):
        Rule.__init__(self)
    def check(self, arg):
        if arg == None:
            return True
        if not isinstance(arg, dict):
            self.set_error(f'"images" is not obj.')
            return False
        
        if arg.get('full_body', None):
            if not url(arg.get('full_body', None)):
                self.set_error(f'"full_body" is not valid url')
                return False
        if arg.get('half_body', None):
            if arg.get('half_body', None):
                if not url(arg.get('half_body', None)):
                    self.set_error(f'"half_body" is not valid url')
                    return False
        else:
            self.set_error(f'"half_body" is required in images.')
            return False

        return True


class Stats(Rule):
    def __init__(self):
        Rule.__init__(self)
    def check(self, arg):
        if not arg:
            self.set_error('Not found stats')
            return False
        if not isinstance(arg, dict):
            self.set_error(f'"stats" is not obj')
            return False
        for name in STATS_NAMES:
            if not name in arg:
                self.set_error(f'Missing "{name}" in stats')
                return False
            if not arg.get(name, None) in STATS_VALUES:
                self.set_error(f'"{name}" is invalid value')
                return False
        return True

