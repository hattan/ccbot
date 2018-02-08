import sys
sys.path.append("ccbot")
from ccbot.services.reddit_client import *
from ccbot.services.api_client import *
from mock_datetime import mock_datetime 
from mock import MagicMock,patch

@patch('ccbot.services.api_client.ApiClient.fetch')
def test_get_data_calls_api_client_fetch(fake_fetch):
    #arrange
    reddit = RedditApiClient("fake_url")
    #act
    data = reddit.get_data()
    #assert
    fake_fetch.assert_called_with(reddit,"fake_url")

@patch('ccbot.services.api_client.ApiClient.fetch')
def test_get_data_extracts_images_from_reddit_response(fake_fetch):
    #arrange
    reddit = RedditApiClient("fake_url")
    fake_fetch.return_value = {"data": {"children": [{"data": {"preview": {"images": [{"source": {"url": "fake_img"}}],}}},{"data": {"preview": {"images": [{"source": {"url": "fake_img2"}}],}}}]}}
    #act
    data = reddit.get_data()
    #assert
    assert data == ['fake_img','fake_img2'] 

def test_fetch():
    #arrange
    reddit = RedditApiClient("fake_url")
    reddit.get_data = MagicMock(return_value=['url'])
    #act
    attachment = reddit.fetch()
    #assert
    assert attachment == [{"title": "url", "image_url": "url"}]
