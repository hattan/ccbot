import random
import sys
sys.path.append("ccbot")

from ccbot.commands.Aww import Aww
from ccbot.services.api_client import *
from ccbot.services.reddit_client import RedditApiClient
from services.slack_response import SlackResponse
from mock import MagicMock,patch

def test_commandtext_is_xkcd():
    assert Aww().get_command() == "aww"

def test_available_in_all_channels():
    assert Aww().get_channel_id() == "all"

def test_invoke_calls_redditclient_fetch_attachment_returned():
    reddit_client = RedditApiClient("fakeurl")
    reddit_client.fetch = MagicMock(return_value=['test'])
    a = Aww()
    a.reddit_client=reddit_client
    text,attachments = a.invoke("aww","fakeuser")
    assert attachments == ['test']   

def test_invoke_calls_redditclient_fetch_text_is_none():
    reddit_client = RedditApiClient("fakeurl")
    reddit_client.fetch = MagicMock(return_value=['test'])
    a = Aww()
    a.reddit_client=reddit_client

    text,attachments = a.invoke("aww","fakeuser")
    assert text is None

def test_invoke_creates_new_reddit_client_if_it_is_None():
    a = Aww()
    a.fetch_data = MagicMock(return_value=['test'])
    text,attachments = a.invoke("aww","fakeuser")
    assert a.reddit_client is not None     