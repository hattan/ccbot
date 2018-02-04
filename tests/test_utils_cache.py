import uuid
import sys
sys.path.append("ccbot")
from mock import MagicMock
from utils.cache import memoize

def test_memoize():
    called=False
    def foo(a):
        return uuid.uuid1()

    f = memoize(foo)

    id = f(3)

    #call should be cached because we did not get a new uuid
    assert id ==  f(3)
