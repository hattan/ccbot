import random
import sys

sys.path.append("ccbot")

from ccbot.commands.TacoMe import TacoMe
from ccbot.services.api_client import *
from services.slack_response import SlackResponse
from mock import MagicMock, patch

COMMAND = 'tacome 90405'


def test_commandtext_is_tacome():
    assert TacoMe().get_command() == "tacome"


def test_available_in_all_channels():
    assert TacoMe().get_channel_id() == "all"


def test_invoke_without_zip_returns_suggestion():
    result = TacoMe().invoke("tacome", "fake_user")
    assert result[0] == 'Try: `tacome _ZIP_CODE_`. Example: `tacome 90405`'



def test_invoke_returns_attachment():
    result = TacoMe().invoke(COMMAND, "fake_user")
    for entry in ('title', 'image_url', 'text'):
        assert result[1][0][entry]


def test_get_auth_value_returns_bearer():
    result = TacoMe().get_auth_value()
    assert result.startswith('Bearer ')


def test_get_zipcode_extracts_5digits():
    cases = {
        'tacome': None,
        'tacome 12345': '12345',
        'tacome   12345': '12345',
        'tacome   12345   ': '12345',
        'tacome 1234': None,
        'tacome 123456': None,
        'tacome a 123456': None,

    }
    
    for command,expected in cases.iteritems():
        actual = TacoMe().get_zipcode(command)
        if (expected is None):
                assert actual is None
        else:
                assert actual == expected 