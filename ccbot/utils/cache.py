import datetime
from functools import wraps

def memoize(function):
    memo = {}
    @wraps(function)
    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
            memo[args] = rv
            return rv
    return wrapper

def wrapped_memoize(function):
    f = memoize(function)
    @wraps(f)
    def wrapper(*args):
        rv = f(*args)
        return "hello=="  + str(rv)
    return wrapper

def parameterized_memoize(input):
    def _parameterized_memoize(function):
        f = memoize(function)
        @wraps(f)
        def wrapper(*args):
            rv = f(*args)
            return input + str(rv)
        return wrapper
    return _parameterized_memoize   

def timed_memoize(minutes):
    expires_on =  datetime.datetime.now() + datetime.timedelta(minutes=minutes)
    def _timed_memoize(function):
        d = dict(f=memoize(function))
        @wraps(d['f'])
        def wrapper(*args):
            now = datetime.datetime.now()
            if now > expires_on:
                d['f'] = memoize(function)
            return d['f'](*args)
        return wrapper
    return _timed_memoize      
