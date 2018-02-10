import random
import sys
sys.path.append("ccbot")

from ccbot.commands.Xkcd import Xkcd
from ccbot.services.api_client import *
from ccbot.services.reddit_client import RedditApiClient
from services.slack_response import SlackResponse
from mock import MagicMock,patch

def test_commandtext_is_xkcd():
    assert Xkcd().get_command() == "xkcd"

def test_available_in_all_channels():
    assert Xkcd().get_channel_id() == "all"

def test_fetch_info_calls_fetch_with_default_url_if_comicid_is_not_passed():
    #arrange
    api_client = ApiClient()
    api_client.fetch = MagicMock(return_value='data')
    xkcd = Xkcd()
    xkcd.api_client = api_client
    #act
    data = xkcd.fetch_info()
    #assert
    api_client.fetch.assert_called_with("https://xkcd.com/info.0.json")

def test_fetch_info_calls_fetch_with_default_url_if_comicid_is_None():
    #arrange
    api_client = ApiClient()
    api_client.fetch = MagicMock(return_value='data')
    xkcd = Xkcd()
    xkcd.api_client = api_client
    #act
    data = xkcd.fetch_info(None)
    #assert
    api_client.fetch.assert_called_with("https://xkcd.com/info.0.json")

def test_fetch_info_calls_fetch_with_comic_url_if_comicid_is_number():
    #arrange
    api_client = ApiClient()
    api_client.fetch = MagicMock(return_value='data')
    xkcd = Xkcd()
    xkcd.api_client = api_client
    #act
    data = xkcd.fetch_info(123)
    #assert
    api_client.fetch.assert_called_with("https://xkcd.com/123/info.0.json")

def test_parse_command_parses_command_only():
    #arrange
    xkcd = Xkcd()
    #act
    command,args = xkcd.parse_command("xkcd")
    #assert
    assert command == "xkcd"
    assert len(args) == 0 

def test_parse_command_parses_command_with_single_arg():
    #arrange
    xkcd = Xkcd()
    #act
    command,args = xkcd.parse_command("xkcd latest")
    #assert
    assert command == "xkcd"
    assert len(args) == 1    

def test_parse_command_parses_command_with_single_arg_arg_is_corret():
    #arrange    
    xkcd = Xkcd()
    #act    
    command,args = xkcd.parse_command("xkcd latest")
    #assert    
    assert command == "xkcd"
    assert args[0] == "latest"

def test_invoke_attachment_is_slack_attachment():
    #arrange
    api_client = ApiClient()
    api_client.fetch = MagicMock(return_value = {'num' : 123, 'title': 'fake comic', 'alt' : 'fake alt', 'img' : 'fake_img'})
    xkcd = Xkcd()
    xkcd.api_client = api_client
    #act
    text,attachment = xkcd.invoke("xkcd","fake_user")
    expected_text,expected_attachment = SlackResponse.attachment(title='fake comic',text='fake alt',image_url='fake_img')
    #assert
    assert attachment == expected_attachment

@patch('random.randint')
def test_invoke_call_fetch_info_with_random_int_if_no_args(fake_randint):
    #arrange
    fake_randint.return_value = 22 
    xkcd = Xkcd()
    xkcd.fetch_info =  MagicMock(return_value = {'num' : 123, 'title': 'fake comic', 'alt' : 'fake alt', 'img' : 'fake_img'})
    #act
    text,attachment = xkcd.invoke("xkcd","fake_user")
    #assert 
    xkcd.fetch_info.assert_called_with(22)

def test_invoke_call_fetch_info_with_comic_id_if_arg_is_number():
    #arrange
    xkcd = Xkcd()
    xkcd.fetch_info =  MagicMock(return_value = {'num' : 123, 'title': 'fake comic', 'alt' : 'fake alt', 'img' : 'fake_img'})
    #act
    text,attachment = xkcd.invoke("xkcd 456","fake_user")
    #assert  
    xkcd.fetch_info.assert_called_with('456')

def test_invoke_call_fetch_info_with_latest_comic_id_if_arg_is_latest():
    #arrange
    xkcd = Xkcd()
    xkcd.fetch_info =  MagicMock(return_value = {'num' : 123456, 'title': 'fake comic', 'alt' : 'fake alt', 'img' : 'fake_img'})
    #act
    text,attachment = xkcd.invoke("xkcd latest","fake_user")
    #assert  
    xkcd.fetch_info.assert_called_with(123456)


def test_invoke_text_is_None():
    #arrange
    api_client = ApiClient()
    api_client.fetch = MagicMock(return_value = {'num' : 123, 'title': 'fake comic', 'alt' : 'fake alt', 'img' : 'fake_img'})
    xkcd = Xkcd()
    xkcd.api_client = api_client
    #act
    text,attachment = xkcd.invoke("xkcd","fake_user")
    #assert
    assert not text