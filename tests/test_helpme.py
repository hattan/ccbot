# import random
import sys
sys.path.append("ccbot")

from ccbot.commands.HelpMe import HelpMe

from mock import MagicMock, patch


class SubjectClass:
    """TestSubject class"""

    def __init__(self):
        """Subject Constructor"""
        self.x = 1

fake_commands = {'marklar': SubjectClass()}


def get_target():
    result = HelpMe()
    result.commands = fake_commands
    return result


def test_command_name():
    assert get_target().get_command() == 'helpme'

def test_channel_id():
    assert get_target().get_channel_id() == 'all'

def test_get_listing():
    target = get_target()
    actual = target.get_listing()
    assert '* `marklar`' in actual

def test_get_details():
    actual = get_target().get_details('marklar')
    assert '`marklar`: TestSubject class' == actual

@patch.object(HelpMe, 'get_details')
def test_invoke_details(get_details):
    get_details.return_value = 'ok'
    get_target().invoke('helpme marklar',None)

    get_details.assert_called_with('marklar')

@patch.object(HelpMe, 'get_listing')
def test_invoke_just_helpme(get_listing):
    get_listing.return_value = 'listing'

    text, attachments = get_target().invoke('helpme',None)

    assert text == 'listing'