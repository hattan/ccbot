import random
import sys
sys.path.append("ccbot")

from ccbot.services.BotCommand import BotCommand
from ccbot.services.api_client import *
from ccbot.services.reddit_client import RedditApiClient
from services.slack_response import SlackResponse
from mock import MagicMock,patch

COMMAND_NAME = 'go_me'
CHANNEL_ID = 'all'

def test_command_name_lowercased():
      assert BotCommand('MixedCaseName').get_command() == 'mixedcasename'

def test_get_channel_id():
    assert BotCommand(COMMAND_NAME, CHANNEL_ID).get_channel_id() == CHANNEL_ID

def test_get_command():
      assert BotCommand(COMMAND_NAME,CHANNEL_ID).get_command() == COMMAND_NAME