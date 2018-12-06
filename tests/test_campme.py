# encoding: utf-8
import random
import sys
import os
import urllib2
import copy
sys.path.append("ccbot")

from ccbot.commands.campme import CampMe
from ccbot.services.api_client import ApiClient
from ccbot.services.slack_response import SlackResponse
from mock import MagicMock, patch
import pytest
import unittest
from urllib2 import URLError, HTTPError
from datetime import datetime, timedelta

TODAY = "%02d" % datetime.now().day

COMMAND = 'campme'
COMMAND_WITH_VERB = 'campme now'
COMMAND_FOR_HELP = 'campme help'
COMMAND_SESSIONS_AT = 'campme sessions at 11:15'
SAMPLE_API_RESPONSE = [{
    'Room': 'SLH 102',
    'SessionEnd': '2018-11-11T11:15:00',
    'SessionId': 'a83dca4a-06f8-48b6-a398-e857c74d6a30',
    'SessionName': 'Awesome Code!',
    'SessionStart': '2018-11-11T11:15:00',
    'SpeakerFirstName': 'Bob',
    'SpeakerLastName': 'Bobberson'}]


def get_target():
    return CampMe()


class CampMeTest(unittest.TestCase):

    def test_commandtext_is_campme(self):
        assert get_target().get_command() == "campme"

    def test_available_in_all_channels(self):
        assert get_target().get_channel_id() == "all"

    def test_invoke_without_verb_returns_suggestion(self):
        result = get_target().invoke(COMMAND, "fake_user")
        assert result[0][0:] == CampMe.USAGE_TEXT

    def test_invoke_help_returns_doc(self):
        text, attachments = get_target().invoke(COMMAND_FOR_HELP, None)
        assert text == CampMe.MANUAL

    def test_invoke_with_next(self):
        text, attachments = get_target().invoke(COMMAND + ' next', None)
        assert 'No sessions matching criteria' in attachments[0]['text']

    @patch.object(CampMe, 'get_data')
    def test_invoke_calls_get_data(self, get_data):
        get_data.return_value = SAMPLE_API_RESPONSE
        target = get_target()
        target.invoke(COMMAND_WITH_VERB, "fake_user")

        get_data.assert_called_with(target.URL)

    @patch.object(CampMe, 'get_data')
    def test_invoke_sessions_at(self, get_data):
        sessions = copy.deepcopy(SAMPLE_API_RESPONSE)
        sessions[0]['SessionStart'] = "2018-11-%02dT11:15:00" % datetime.now().day
        get_data.return_value = sessions
        target = get_target()

        _, attachments = target.invoke(COMMAND_SESSIONS_AT, None)

        assert attachments[0]['author_name'] == 'Code Camp Bot'

    @patch.object(CampMe, 'get_data')
    def test_invoke_io_error(self, get_data):
        get_data.side_effect = HTTPError(
            url='http://a.b/', code=403, msg='nope!', hdrs=None, fp=None)
        actual = get_target().invoke(COMMAND_WITH_VERB, "fake_user")
        assert actual == SlackResponse.text('HTTP Error 403: nope!')

    @patch.object(CampMe, 'get_data')
    def test_invoke_value_error(self, get_data):
        get_data.side_effect = URLError('Nope!')
        actual = get_target().invoke(COMMAND_WITH_VERB, "fake_user")
        assert actual == SlackResponse.text("('Nope!',)")

    def test_create_slack_response_populates_attachment(self):
        actual = CampMe.create_slack_response(SAMPLE_API_RESPONSE, 'something')
        for entry in ('title', 'text', 'author_link', 'author_name'):
            assert actual[1][0][entry]

    def test_create_slack_response_zero_results(self):
        actual = CampMe.create_slack_response([], 'something')
        assert actual[0] == 'Server returned no data ¯\\_(ツ)_/¯'

    def test_get_verb_extracts_verb(self):
        cases = {
            'campme': None,
            'campme now': ['now'],
            'campme   now': ['now'],
            'campme   next   ': ['next'],
            'campme speaker bob bobbernaugh': ['speaker', 'bob', 'bobbernaugh'],
            'campme sessions at 12:45': ['sessions', 'at', '12:45']
        }

        for command, expected in cases.iteritems():
            actual = get_target().get_verb(command)
            if (expected is None):
                assert actual is None
            else:
                assert actual == expected

    def test_get_data_calls_api(self):
        api_client = ApiClient()
        api_client.fetch = MagicMock(return_value='yup')

        target = get_target()
        target.api_client = api_client

        actual = target.get_data('dummy_url')

        assert actual == 'yup'
        target.api_client.fetch.assert_called_once()

    def test_is_by_speaker(self):
        cases = [
            (['bob'], True),
            (['BoB'], True),
            (['bob', 'bobbernaugh'], True),
            (['bob', 'jones'], True),
            (['bobbernaugh'], True),
            (['bobbernaugh', 'the great'], True),
            (['ogg'], False),
        ]

        for name_parts, expected in cases:
            r = CampMe.build_regex(name_parts)
            assert expected == CampMe.is_by_speaker(
                {'SpeakerFirstName': 'Bob', 'SpeakerLastName': 'Bobbernaugh'}, r)

    def test_build_regex(self):
        t = CampMe.build_regex(['alpha', 'beta'])
        assert t.pattern == "(\\balpha\\b|\\bbeta\\b)"

    def test_is_at_time(self):
        clock = datetime(2018, 11, 10)
        stated_time = '14:15'
        cases = {
            '2018-11-10T14:15:00': True,
            '2018-11-07T14:15:00': False,  # wrong day wrt clock
            '2018-11-10T08:30:00': False,  # wrong time wrt start_time
        }

        for start, expected in cases.iteritems():
            assert CampMe.is_at_time(
                {'SessionStart': start}, stated_time, clock) == expected

    def test_is_now(self):
        assert CampMe.is_now(
            {'SessionStart': '2000-01-01T00:00:00', 'SessionEnd': '2222-01-01T00:00:00'})

    def test_is_next(self):
        now = datetime.now()
        two_minutes_from_now = now + timedelta(minutes=1)
        two_hours_from_now = now + timedelta(hours=2)

        assert CampMe.is_next(
            self._create_session_timeslot(two_minutes_from_now))

        assert not CampMe.is_next(self._create_session_timeslot(now))

        assert not CampMe.is_next(
            self._create_session_timeslot(two_hours_from_now))

    def _create_session_timeslot(self, dt):
        result = {
            'SessionStart': datetime.strftime(dt, "%Y-%m-%dT%H:%M:%S"),
            'SessionEnd': datetime.strftime(dt + timedelta(hours=1, minutes=15), "%Y-%m-%dT%H:%M:%S")
        }
        return result

    def test_nice(self):
        assert CampMe.nice('2000-01-01T13:45:00') == 'Sat 13:45'

    def test_format_text_when_no_items(self):
        assert CampMe.format_text([]) == CampMe.NO_MATCHES_FOUND

    def test_format_when_items(self):
        assert CampMe.format_text(SAMPLE_API_RESPONSE, False).startswith(
            'Sun 11:15 - Sun 11:15')

    def test_format_when_by_speaker(self):
        assert CampMe.format_text(SAMPLE_API_RESPONSE, True).startswith(
            '*  Bob Bobberson: Awesome Code!  @ SLH 102 Sun 11:15')
    
    def test_filter_items_speaker(self):
        actual =  CampMe.filter_items(SAMPLE_API_RESPONSE, ('speaker','Dwain', 'Bobberson'))[0]
        
        assert actual['SpeakerLastName'] == 'Bobberson'
