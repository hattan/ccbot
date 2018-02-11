import sys
sys.path.append("ccbot")

from ccbot.commands.catme import CatMe
from services.api_client import ApiClient

from mock import MagicMock

def test_catme_url_is_edgecats_github_repo_contents():
    assert CatMe().url == "https://api.github.com/repos/flores/moarcats/contents/cats?ref=master"

def test_catme_commandtext_is_catme():
    assert CatMe().get_command() == "catme"    

def test_catme_available_in_all_channels():
    assert CatMe().get_channel_id() == "all"  

def test_catme_invoke_calls_api_client_fetch_returns_edgecats_url():
    api_client = ApiClient()
    api_client.fetch = MagicMock(return_value=[{"name" : "foo"}])
    catme = CatMe()
    catme.api_client=api_client
    text,attachments = catme.invoke("catme","fakeuser")
    assert attachments == [{"title": "http://edgecats.net/cats/foo", "image_url": "http://edgecats.net/cats/foo"}]      

def test_catme_invoke_calls_api_client_fetch_text_is_none():
    api_client = ApiClient()
    api_client.fetch = MagicMock(return_value=[{"name" : "foo"}])
    catme = CatMe()
    catme.api_client=api_client
    text,attachments = catme.invoke("catme","fakeuser")
    assert text is None