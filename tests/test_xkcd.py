import sys
sys.path.append("ccbot")

from ccbot.commands.Xkcd import Xkcd
from ccbot.services.api_client import *
from ccbot.services.reddit_client import RedditApiClient

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
    xkcd = Xkcd()
    command,args = xkcd.parse_command("xkcd")
    assert command == "xkcd"
    assert len(args) == 0 

def test_parse_command_parses_command_with_single_arg():
    xkcd = Xkcd()
    command,args = xkcd.parse_command("xkcd latest")
    assert command == "xkcd"
    assert len(args) == 1    

def test_parse_command_parses_command_with_single_arg_arg_is_corret():
    xkcd = Xkcd()
    command,args = xkcd.parse_command("xkcd latest")
    assert command == "xkcd"
    assert args[0] == "latest"
