import uuid
import sys
sys.path.append("ccbot")
from mock import MagicMock
from utils.cache import memoize,wrapped_memorize

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
    f = wrapped_memorize(foo)
    id = f(3)
    assert id == f(3)
    assert id.startswith("hello==")


