# import random
import sys
sys.path.append("ccbot")

from ccbot.services.help_factory import HelpFactory

from ccbot.services.slack_response import SlackResponse
from mock import MagicMock, patch


class SubjectClass:
    """TestSubject class"""

    def __init__(self):
        """Subject Constructor"""
        self.x = 1


class UndocumentedClass:
    def __init__(self):
        pass


def get_target():
    return HelpFactory({'TestSubject': SubjectClass()})


def test_list_returns_command_names():
    assert get_target().list()[0] == 'TestSubject'


def test_details_returns_doc_from_command():
    actual = get_target().details('TestSubject')
    assert actual == 'TestSubject class'


def test_details_no_doc_returns_command_name():
    actual = HelpFactory(
        {'Undocumented': UndocumentedClass()}
    ).details('Undocumented')
    
    assert actual == 'Undocumented'
