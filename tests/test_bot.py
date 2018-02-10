import random
import sys
import os
import glob
import importlib
import inspect
import time
sys.path.append("ccbot")

from ccbot.bot import *
from ccbot.services.api_client import *
from ccbot.services.reddit_client import RedditApiClient
from services.slack_response import SlackResponse
from mock import MagicMock,patch

@patch('os.path.join')
@patch('glob.glob')
def test_load_commands_glob_called_with_current_dir(fake_glob,fake_join):
    #arrange
    fake_join.return_value = "fake_dir"  #set the current_dir (returned from path.join)
    #act
    load_commands()
    #assert
    fake_glob.assert_called_with('fake_dir/commands/*.py')




