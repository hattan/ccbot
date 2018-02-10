import sys
sys.path.append("ccbot")

from ccbot.commands.tortoiseme import TortoiseMe
from ccbot.services.reddit_client import RedditApiClient

from mock import MagicMock

def test_url_is_tortoise_subreddit():
    assert TortoiseMe().url == "https://www.reddit.com/r/tortoise.json"
    
def test_commandtext_is_tortoiseme():
    assert TortoiseMe().get_command() == "tortoiseme"

def test_available_in_all_channels():
    assert TortoiseMe().get_channel_id() == "all"

def test_invoke_calls_redditclient_fetch_attachment_returned():
    reddit_client = RedditApiClient("fakeurl")
    reddit_client.fetch = MagicMock(return_value=['test'])
    t = TortoiseMe()
    t.reddit_client=reddit_client
    text,attachments = t.invoke("tortoiseme","fakeuser")
    assert attachments == ['test']   

def test_invoke_calls_redditclient_fetch_text_is_none():
    reddit_client = RedditApiClient("fakeurl")
    reddit_client.fetch = MagicMock(return_value=['test'])
    t = TortoiseMe()
    t.reddit_client=reddit_client

    text,attachments = t.invoke("dogme","fakeuser")
    assert text is None

def test_invoke_creates_new_reddit_client_if_it_is_None():
    t = TortoiseMe()
    t.fetch_data = MagicMock(return_value=['test'])
    text,attachments = t.invoke("dogme","fakeuser")
    assert t.reddit_client is not None 