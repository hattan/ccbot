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
    f = timed_memoize(2)(foo)
    
    #verify
    id = f(3)
    assert id == f(3)

    target = datetime.datetime.now() + datetime.timedelta(minutes=5)
    with mock_datetime(target, datetime):
        assert id != f(3) #should no longer be cached

def test_timed_memoize_method_not_called_before_expiry_time():
    #arrange
    def foo(a):
        return uuid.uuid1()
    f = timed_memoize(10)(foo)
    
    #act
    id = f(3)

    #assert
    target = datetime.datetime.now() + datetime.timedelta(minutes=1)
    with mock_datetime(target, datetime):
        assert id == f(3) #should still be cached      


def test_timed_memoize_method_resets_expiry_time():
    #arrange
    def foo(a):
        return uuid.uuid1()
    f = timed_memoize(10)(foo)
    
    #act
    id = f(3)

    #assert
    target = datetime.datetime.now() + datetime.timedelta(minutes=11)
    with mock_datetime(target, datetime):
        tmp = id
        id = f(3)
        assert id != tmp #should not be cached    

    #assert
    target = datetime.datetime.now() + datetime.timedelta(minutes=12)
    with mock_datetime(target, datetime):
        assert id == f(3) #should  be cached    

def test_timed_memoize_multiple_instances_should_not_collide():
    #arrange
    def foo(a):
        return uuid.uuid1()
    f = timed_memoize(10)(foo)
    b = timed_memoize(2)(foo)
    #act
    fid = f(3)
    bid = b(3)
    #assert
    target = datetime.datetime.now() + datetime.timedelta(minutes=11)
    with mock_datetime(target, datetime):
        assert fid != f(3) #should not be cached    

    target = datetime.datetime.now() + datetime.timedelta(minutes=1)
    with mock_datetime(target, datetime):
        assert bid == b(3) #should  be cached   

    