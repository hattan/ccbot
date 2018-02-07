import uuid
import datetime
import sys
sys.path.append("ccbot")
from mock_datetime import mock_datetime 
from mock import MagicMock
from time import sleep
from ccbot.services.slack_response import *


def test_attachment_sets_pretext():
    #arrange
    pre_text = "preprepre"

    #act
    text,attachment = SlackResponse.attachment(pretext = pre_text)

    #assert
    assert attachment == [{'pretext' : pre_text}]

def test_attachment_sets_text():
    #arrange
    t = "ttt"

    #act
    text,attachment = SlackResponse.attachment(text = t)

    #assert
    assert attachment == [{'text' : t}]
