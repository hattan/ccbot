import sys
sys.path.append("ccbot")

from ccbot.commands.Xkcd import Xkcd
from ccbot.services.reddit_client import RedditApiClient

from mock import MagicMock

def test_commandtext_is_xkcd():
    assert Xkcd().get_command() == "xkcd"

def test_available_in_all_channels():
    assert Xkcd().get_channel_id() == "all"