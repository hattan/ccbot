import random
import sys
import os
import glob
import importlib
import inspect
import time

sys.path.append("ccbot")

from slackclient import SlackClient
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

@patch('slackclient.SlackClient.api_call')
@patch('ccbot.commands.Aww.Aww.invoke')
def test_handle_command_calls_slack_api_call_with_attachment(fake_aww_invoke,fake_slack_api_call):
    #arrange
    aww = Aww()
    commands[aww.get_command()] = aww
    user = "fake_user"
    channel = "fake_channel"
    text, attachment = SlackResponse.attachment(title="foo")
    fake_aww_invoke.return_value = text, attachment
    #act
    handle_command("aww",channel,user)
    #assert
    fake_slack_api_call.assert_called_with('chat.postMessage', as_user=True, attachments=attachment, channel=channel, text='')

@patch('slackclient.SlackClient.api_call')
@patch('ccbot.commands.Aww.Aww.invoke')
def test_handle_command_calls_slack_api_call_with_text(fake_aww_invoke,fake_slack_api_call):
    #arrange
    aww = Aww()
    commands[aww.get_command()] = aww
    user = "fake_user"
    channel = "fake_channel"
    text, attachment = SlackResponse.text("bar")
    fake_aww_invoke.return_value = text, attachment
    #act
    handle_command("aww",channel,user)
    #assert
    fake_slack_api_call.assert_called_with('chat.postMessage', channel=channel, text=text,as_user=True)
    
@patch('slackclient.SlackClient.api_call')
@patch('ccbot.commands.Aww.Aww.invoke')
def test_handle_command_with_empty_string_does_not_call_slack(fake_aww_invoke,fake_slack_api_call):
    #arrange
    aww = Aww()
    commands[aww.get_command()] = aww
    user = "fake_user"
    channel = "fake_channel"
    text, attachment = SlackResponse.text("bar")
    fake_aww_invoke.return_value = text, attachment
    #act
    handle_command("",channel,user)
    #assert
    assert not fake_slack_api_call.called
    assert not fake_aww_invoke.called

def test_parse_slack_output_returns_none_if_rtm_output_is_none():
    #arrange
    #act
    command,channel,user = parse_slack_output(None)
    #assert
    assert not command 
    assert not channel
    assert not user

def test_parse_slack_output_returns_command_channel_user_from_rtm_output():
    #arrange
    rtm_output = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]
    #act
    command,channel,user = parse_slack_output(rtm_output)
    #assert
    assert command == 'test 123'
    assert channel == 'foo'
    assert user == 'bar'

@patch('ccbot.bot.load_commands')
@patch('slackclient.SlackClient.rtm_connect')
def test_start_bot_loads_commands(fake_rtm_connect,fake_load_commands):
    #arrange
    fake_load_commands.return_value = None
    fake_rtm_connect.return_value = False
    #act
    start_bot()
    #assert
    assert fake_load_commands.called

@patch('ccbot.bot.load_commands')
@patch('slackclient.SlackClient.rtm_connect')
def test_start_bot_prints_message_if_slack_client_cant_connect(fake_rtm_connect,fake_load_commands,capsys):
    #arrange
    fake_load_commands.return_value = None
    fake_rtm_connect.return_value = False
    #act
    start_bot()
    #assert
    out, err = capsys.readouterr()
    assert out == "Connection failed. Invalid Slack token or bot ID?\n"

@patch('ccbot.bot.load_commands')
@patch('slackclient.SlackClient.rtm_connect')
def test_start_bot_prints_message_if_slack_client_cant_connect(fake_rtm_connect,fake_load_commands,capsys):
    #arrange
    fake_load_commands.return_value = None
    fake_rtm_connect.return_value = False
    #act
    start_bot()
    #assert
    out, err = capsys.readouterr()
    assert out == "Connection failed. Invalid Slack token or bot ID?\n"    

count = 0
def fake_runner():
    global count 
    count = count + 1
    return count < 2

@patch('ccbot.bot.running') 
@patch('ccbot.bot.load_commands')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.rtm_read')
@patch('ccbot.bot.get_sleep_time')
def test_start_bot_success_prints_connected_message(fake_get_sleep_time,fake_rtm_read,fake_rtm_connect,fake_load_commands,fake_running,capsys):
    #arrange
    global count 
    count = 0
    fake_running.side_effect=fake_runner
    fake_load_commands.return_value = None
    fake_rtm_connect.return_value = True
    fake_get_sleep_time.return_value = 0.001    
    fake_rtm_read.return_value = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]
    #act
    start_bot()
    #assert
    out, err = capsys.readouterr()
    assert out == (BOT_NAME + " connected and running!\n")   

@patch('ccbot.bot.running')
@patch('ccbot.bot.load_commands')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.rtm_read')
@patch('ccbot.bot.parse_slack_output')
@patch('ccbot.bot.get_sleep_time')
def test_start_bot_calls_parse_slack_output(fake_get_sleep_time,fake_parse_slack_output,fake_rtm_read,fake_rtm_connect,fake_load_commands,fake_running):
    #arrange
    global count 
    count = 0
    fake_parse_slack_output.return_value = 'test','test','test'
    fake_running.side_effect=fake_runner
    fake_load_commands.return_value = None
    fake_rtm_connect.return_value = True
    fake_get_sleep_time.return_value = 0.001
    fake_rtm_read.return_value = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]
    #act
    start_bot()
    #assert
    fake_parse_slack_output.assert_called_with([{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}])

@patch('ccbot.bot.running')
@patch('ccbot.bot.load_commands')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.rtm_read')
@patch('ccbot.bot.handle_command')
@patch('ccbot.bot.get_sleep_time')
def test_start_bot_calls_handle_command(fake_get_sleep_time,fake_handle_command,fake_rtm_read,fake_rtm_connect,fake_load_commands,fake_running):
    #arrange
    global count 
    count = 0
    fake_running.side_effect=fake_runner
    fake_load_commands.return_value = None
    fake_rtm_connect.return_value = True
    fake_get_sleep_time.return_value = 0.001
    fake_rtm_read.return_value = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]
    #act
    start_bot()
    #assert
    fake_handle_command.assert_called_with('test 123','foo','bar')    

@patch('ccbot.bot.running')
@patch('ccbot.bot.load_commands')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.rtm_read')
@patch('ccbot.bot.handle_command')
@patch('time.sleep')
@patch('ccbot.bot.get_sleep_time')
def test_start_bot_time_sleep_called_with_expected_value(fake_get_sleep_time,fake_sleep,fake_handle_command,fake_rtm_read,fake_rtm_connect,fake_load_commands,fake_running):
    #arrange
    global count 
    count = 0
    fake_running.side_effect=fake_runner
    fake_load_commands.return_value = None
    fake_rtm_connect.return_value = True
    fake_get_sleep_time.return_value = 0.001
    fake_rtm_read.return_value = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]
    #act
    start_bot()
    #assert
    fake_sleep.assert_called_with(0.001)    

def test_running_returns_true():
    #arrange
    #act
    result = running()
    #assert
    assert running

def test_get_sleep_time_one_minute():
    #arrange
    #act
    result = get_sleep_time()
    #assert
    assert result == 1
     




    




