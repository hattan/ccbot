import random
import sys
sys.path.append("ccbot")

from ccbot.commands.TeslaMe import TeslaMe
from ccbot.services.api_client import *
from ccbot.services.reddit_client import RedditApiClient
from services.slack_response import SlackResponse
from mock import MagicMock,patch

def test_commandtext_is_xkcd():
    assert TeslaMe().get_command() == "teslame"

def test_available_in_all_channels():
    assert TeslaMe().get_channel_id() == "all"

def test_invoke_calls_redditclient_fetch_attachment_returned():
    reddit_client = RedditApiClient("fakeurl")
    reddit_client.fetch = MagicMock(return_value=['test'])
    t = TeslaMe()
    t.reddit_client=reddit_client
    text,attachments = t.invoke("teslame","fakeuser")
    assert attachments == ['test']   

def test_invoke_calls_redditclient_fetch_text_is_none():
    reddit_client = RedditApiClient("fakeurl")
    reddit_client.fetch = MagicMock(return_value=['test'])
    t = TeslaMe()
    t.reddit_client=reddit_client

    text,attachments = t.invoke("teslame","fakeuser")
    assert text is None

def test_invoke_creates_new_reddit_client_if_it_is_None():
    t = TeslaMe()
    t.fetch_data = MagicMock(return_value=['test'])
    text,attachments = t.invoke("teslame","fakeuser")
    assert t.reddit_client is not None     