import sys
sys.path.append("ccbot")

from ccbot.commands.catme import CatMe
from services.api_client import ApiClient

from mock import MagicMock

def test_catme_url_is_edgecats_github_repo_contents():
    assert CatMe().cats_url == "https://api.github.com/repos/flores/moarcats/contents/cats?ref=master"

def test_catme_commandtext_is_catme():
    assert CatMe().get_command() == "catme"    

def test_catme_available_in_all_channels():
    assert CatMe().get_channel_id() == "all"  
