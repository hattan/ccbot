import random
import sys

sys.path.append("ccbot")

from ccbot.commands.TacoMe import TacoMe
from ccbot.services.api_client import *
from services.slack_response import SlackResponse
from mock import MagicMock,patch

COMMAND = 'tacome 90405'

def test_commandtext_is_tacome():
    assert TacoMe().get_command() == "tacome"

def test_available_in_all_channels():
    assert TacoMe().get_channel_id() == "all"


def test_invoke_returns_title():
    result = TacoMe().invoke(COMMAND, "fake_user")
    for entry in ('title', 'image_url', 'text'):
        assert result[1][0][entry]

def test_get_auth_value_returns_bearer():
    result = TacoMe().get_auth_value()
    assert result.startswith('Bearer ')