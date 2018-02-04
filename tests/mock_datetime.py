#from - https://solidgeargroup.com/mocking-the-time
import datetime
import mock

real_datetime_class = datetime.datetime

def mock_datetime(target, datetime_module):
    class DatetimeSubclassMeta(type):
        @classmethod
        def __instancecheck__(mcs, obj):
            return isinstance(obj, real_datetime_class)

    class BaseMockedDatetime(real_datetime_class):
        @classmethod
        def now(cls, tz=None):
            return target.replace(tzinfo=tz)

        @classmethod
        def utcnow(cls):
            return target

        @classmethod
        def today(cls):
            return target

    # Python2 & Python3-compatible metaclass
    MockedDatetime = DatetimeSubclassMeta('datetime', (BaseMockedDatetime,), {})

    return mock.patch.object(datetime_module, 'datetime', MockedDatetime)