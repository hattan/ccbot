import sys
sys.path.append("ccbot")
from ccbot.services.reddit_client import *
from ccbot.services.api_client import *
from mock_datetime import mock_datetime 
from mock import MagicMock,patch

@patch('ccbot.services.api_client.ApiClient.fetch')
def test_get_data(fake_fetch):
    #arrange
    reddit = RedditApiClient("fake_url")
    #act
    data = reddit.get_data()
    #assert
    fake_fetch.assert_called_with(reddit,"fake_url")

def test_fetch():
    #arrange
    reddit = RedditApiClient("fake_url")
    reddit.get_data = MagicMock(return_value=['url'])
    #act
    attachment = reddit.fetch()
    #assert
    assert attachment == [{"title": "url", "image_url": "url"}]
