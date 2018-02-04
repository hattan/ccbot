import uuid
import datetime
import sys
sys.path.append("ccbot")
from mock_datetime import mock_datetime 
from mock import MagicMock
from time import sleep
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

def test_timed_memoize_method_called_after_expiry_time():
    #do
    def foo(a):
        return uuid.uuid1()
    duration =  1 #second
    now = datetime.datetime.now()
    expires_on =  now + datetime.timedelta(minutes=2)
    f = timed_memoize(expires_on)(foo)
    
    #verify
    id = f(3)
    assert id == f(3)

    five_minutes = datetime.timedelta(minutes=5)
    target = now + five_minutes
    with mock_datetime(target, datetime):
        assert id != f(3) #should no longer be cached

def test_timed_memoize_method_not_called_before_expiry_time():
    #arrange
    def foo(a):
        return uuid.uuid1()
    duration =  1 #second
    now = datetime.datetime.now()
    expires_on =  now + datetime.timedelta(minutes=10)
    f = timed_memoize(expires_on)(foo)
    
    #act
    id = f(3)

    #assert
    target = now + datetime.timedelta(minutes=5)
    with mock_datetime(target, datetime):
        assert id == f(3) #should still be cached      

    