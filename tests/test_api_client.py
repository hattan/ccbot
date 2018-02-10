import sys
sys.path.append("ccbot")
import urllib2
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

@patch('ccbot.services.api_client.ApiClient.fetch_raw')
def test_fetch_calls_fetch_raw_with_corresponding_url_no_headers(fake_fetch_raw):
    #arrange
    url = "fake_url"
    reddit = ApiClient()
    fake_fetch_raw.return_value = "{\"data\":\"foo\"}"
    #act
    data = reddit.fetch(url)
    #assert
    fake_fetch_raw.assert_called_with(url,None)

@patch('urllib2.Request')
@patch('urllib2.urlopen')
def test_fetch_raw_creates_urllib2_request(fake_urlopen,fake_request):
    #arrange
    url = "fake_url"
    headers = {"Accept" : "foobar"}
    req = FakeRequest()
    reddit = ApiClient()
    fake_request.return_value = req
    #act
    data = reddit.fetch_raw(url,headers)
    #assert
    fake_request.assert_called_with(url)    
    fake_urlopen.assert_called_with(req)  

class FakeRequest:
    headers = {}
    def add_header(self,key,value):
        self.headers[key]=value
    def get_type(self):
        return ""
    def read(self):
        return ""
    