import sys
sys.path.append("ccbot")

from ccbot.commands.dogme import DogMe
from ccbot.services.reddit_client import RedditApiClient

from mock import MagicMock

def test_dogme_url_is_puppies_subreddit():
    dogme = DogMe()
    assert dogme.url == "https://www.reddit.com/r/puppies.json"
    
def test_dogme_commandtext_is_dogme():
    dogme = DogMe()
    command_text = dogme.get_command()
    assert command_text == "dogme"

def test_dogme_available_in_all_channels():
    dogme = DogMe()
    channel = dogme.get_channel_id()
    assert channel == "all"

def test_dogme_invoke_calls_redditclient_fetch_attachment_returned():
    reddit_client = RedditApiClient("fakeurl")
    reddit_client.fetch = MagicMock(return_value=['test'])
    dogme = DogMe()
    dogme.reddit_client=reddit_client
    text,attachments = dogme.invoke("dogme","fakeuser")
    assert attachments == ['test']   

def test_dogme_invoke_calls_redditclient_fetch_text_is_none():
    reddit_client = RedditApiClient("fakeurl")
    reddit_client.fetch = MagicMock(return_value=['test'])
    dogme = DogMe()
    dogme.reddit_client=reddit_client

    text,attachments = dogme.invoke("dogme","fakeuser")
    assert text is None

def test_dogme_invoke_creates_new_reddit_client_if_it_is_None():
    dogme = DogMe()
    dogme.fetch_data = MagicMock(return_value=['test'])
    text,attachments = dogme.invoke("dogme","fakeuser")
    assert dogme.reddit_client is not None 