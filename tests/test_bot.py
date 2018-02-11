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

@patch('os.path.join')
@patch('glob.glob')
@patch('importlib.import_module')
def test_load_commands_ignores_name_starts_with_double_underscore(fake_import_module,fake_glob,fake_join):
    #arrange
    fake_join.return_value = "fake_dir" 
    fake_glob.return_value = ["__init__.py"]
    fake_import_module.return_value=Aww()
    #act
    load_commands()
    #assert
    assert not fake_import_module.called

def side_effect(input):
  return True if str(input) == "ccbot.commands.Aww.Aww" else False

@patch('os.path.join')
@patch('glob.glob')
@patch('importlib.import_module')
@patch('inspect.isclass')
@patch('ccbot.bot.is_command')
@patch('ccbot.bot.get_class')
def test_load_commands_adds_imported_module_to_commands_list(fake_get_class,fake_is_command,fake_isclass,fake_import_module,fake_glob,fake_join):
    #arrange
    fake_join.return_value = "fake_dir" 
    fake_glob.return_value = ["FooBar.py"]
    fake_import_module.return_value = Aww
    fake_isclass.return_value=True
    fake_is_command.side_effect = side_effect
    fake_get_class.return_value = Aww
    #act
    load_commands()
    #assert
    assert len(commands) == 1
    assert Aww().get_command() in commands
    assert type(commands[Aww().get_command()]) == type(Aww())

  



    




