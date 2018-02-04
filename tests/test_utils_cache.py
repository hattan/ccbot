import uuid
import sys
sys.path.append("ccbot")
from mock import MagicMock
from utils.cache import *

def test_memoize():
    def foo(a):
        return uuid.uuid1()
    f = memoize(foo)
    id = f(3)
    #call should be cached because we did not get a new uuid
    assert id ==  f(3)

def test_wraped_memoize_decorator():
    def foo(a):
        return uuid.uuid1()
    f = wrapped_memoize(foo)
    id = f(3)
    assert id == f(3)
    assert id.startswith("hello==")

def test_parameterized_memoize():
    def foo(a):
        return uuid.uuid1()
    random_str = str(uuid.uuid1())
    f = parameterized_memoize(random_str)(foo)
    id = f(3)
    assert id == f(3)
    assert id.startswith(random_str) 