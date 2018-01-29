from commands.dogme import DogMe
from services.reddit_client import RedditApiClient
from mock import MagicMock

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