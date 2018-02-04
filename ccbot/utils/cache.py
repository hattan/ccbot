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

def wrapped_memorize(function):
    f = memoize(function)
    @wraps(f)
    def wrapper(*args):
        rv = f(*args)
        return "hello=="  + str(rv)
    return wrapper