import sys
sys.path.append("ccbot")

from ccbot.commands.goatme import GoatMe
from services.api_client import ApiClient
from utils.cache import *

from mock import MagicMock

def test_goatme_url_is_puppies_subreddit():
    assert GoatMe().url == "https://api.imgur.com/3/gallery/r/babygoats"
    
def test_goatme_commandtext_is_dogme():
    assert GoatMe().get_command() == "goatme"

def test_goatme_available_in_all_channels():
    assert GoatMe().get_channel_id() == "all"