import random
import sys
import os
import glob
import importlib
import inspect
import time
sys.path.append("ccbot")

from ccbot.bot import *
from ccbot.commands.Aww import Aww
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

@patch('os.path.join')
@patch('glob.glob')
@patch('importlib.import_module')
def test_load_commands_import_module_called_with_name(fake_import_module,fake_glob,fake_join):
    #arrange
    fake_join.return_value = "fake_dir" 
    fake_glob.return_value = ["FooBar.py"]
    fake_import_module.return_value=Aww()
    #act
    load_commands()
    #assert
    fake_import_module.assert_called_with('.FooBar',package="commands")    

def side_effect(input):
  return True if input == "ccbot.commands.Aww" else False







