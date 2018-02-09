import sys
sys.path.append("ccbot")
from ccbot.services.reddit_client import *
from ccbot.services.api_client import *
from mock_datetime import mock_datetime 
from mock import MagicMock,patch

@patch('ccbot.services.api_client.ApiClient.fetch_raw')
def test_fetch_calls_fetch_raw_and_decodes_json(fake_fetch_raw):
    #arrange
    reddit = ApiClient()
    fake_fetch_raw.return_value = "{\"data\":\"foo\"}"
    #act
    data = reddit.fetch("fake_url")
    #assert
    assert data == {"data" : "foo"}

