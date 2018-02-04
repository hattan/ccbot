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
