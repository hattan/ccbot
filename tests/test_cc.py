import uuid
import sys
import mock
import os
sys.path.append("ccbot")

from ccbot.commands.cc import CCBot
from services.api_client import ApiClient
from utils.cache import *
from mock_datetime import mock_datetime 
from mock import MagicMock

def test_ccbot_commandtext_is_dogme():
    assert CCBot().get_command() == "ccbot"

def test_ccbot_available_in_all_channels():
    assert CCBot().get_channel_id() == "all"

def test_ccbot_init_creates_new_api_client():
    cc_bot = CCBot()
    assert cc_bot.api_client is not None

def test_ccbot_parse_command_parses_command_only():
    cc_bot = CCBot()
    command,action,args = cc_bot .parse_command("ccbot")
    assert command == "ccbot"
    assert action is None
    assert len(args) == 0 

def test_ccbot_parse_command_parses_command_and_action():
    cc_bot = CCBot()
    command,action,args = cc_bot .parse_command("ccbot foobar")
    assert command == "ccbot"
    assert action == "foobar"
    assert len(args) == 0 

def test_ccbot_parse_command_parses_command_and_action_and_args():
    cc_bot = CCBot()
    command,action,args = cc_bot .parse_command("ccbot foobar 1 2 3")
    assert command == "ccbot"
    assert action == "foobar"
    assert len(args) == 3
    assert args == ['1','2','3']

def test_invoke_calls_corresponding_action_method():
    cc_bot = CCBot()
    cc_bot.action_foo = MagicMock(return_value='b')
    text,attachments = cc_bot.invoke("ccbot foo", "fakeuser")
    assert text == "b"

def test_invoke_returns_bully_response_if_user_is_bully_and_action_not_found():
    cc_bot = CCBot()
    cc_bot.deny_response = ['bully response']
    text,attachments = cc_bot.invoke("ccbot boo", cc_bot.bully_id)
    assert text == "bully response"

def test_invoke_returns_bully_response_with_bully_name():
    cc_bot = CCBot()
    bully_name = cc_bot.bully_name
    cc_bot.deny_response = ['bully is {name}']
    text,attachments = cc_bot.invoke("ccbot boo", cc_bot.bully_id)
    assert text == 'bully is ' + bully_name

def test_invoke_returns_bully_response_with_action():
    cc_bot = CCBot()
    action = "marklar"
    cc_bot.deny_response = ['bully is trying to {action}']
    text,attachments = cc_bot.invoke("ccbot " + action, cc_bot.bully_id)
    assert text == ('bully is trying to %(action)s' % {'action' : action})

def test_invoke_returns_bully_response_with_action_and_bully_name():
    cc_bot = CCBot()
    action = "marklar"
    bully_name = cc_bot.bully_name
    cc_bot.deny_response = ['bully {name} is trying to {action}']
    text,attachments = cc_bot.invoke("ccbot " + action, cc_bot.bully_id)
    assert text == ('bully %(bully_name)s is trying to %(action)s' % {'action' : action, 'bully_name' : bully_name})

#action tests
def test_ccbot_action_get_time_returns_current_time():
    cc_bot = CCBot()
    now = datetime.datetime.now() 
    target = now
    with mock_datetime(target, datetime): 
        assert cc_bot.action_get_time(None) == now.strftime('%Y-%m-%d %H:%M:%S')

def test_ccbot_action_schedule_returns_code_camp_schedule_link():
    cc_bot = CCBot()
    assert cc_bot.action_schedule() == "https://www.socalcodecamp.com/schedule.aspx"

def test_action_telljoke_calls_api_client_fetch():
    joke = 'ha ha, great joke!'
    cc_bot = CCBot()
    api_client = ApiClient()
    api_client.fetch_raw = MagicMock(return_value=joke)
    cc_bot.api_client = api_client
    response = cc_bot.action_telljoke(None)
    assert response == joke

#def test_action_telljoke_calls_api_client_fetch_with_accept_header():

def test_action_debug_bully_id_returns_bully_id():
    cc_bot = CCBot()
    result = cc_bot.action_debug_bully_id()
    assert result == cc_bot.bully_id

def test_action_debug_bully_id_returns_bully_name():
    cc_bot = CCBot()
    result = cc_bot.action_debug_bully_name()
    assert result == cc_bot.bully_name




