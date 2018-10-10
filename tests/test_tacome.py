import random
import sys
import os

sys.path.append("ccbot")

from ccbot.commands.TacoMe import TacoMe
# from ccbot.services.api_client import *
from ccbot.services.slack_response import SlackResponse
from mock import MagicMock, patch
import pytest
import unittest

ZIP = '90405'
COMMAND = 'tacome ' + ZIP
API_RESPONSE_SAMPLE = {'businesses': [
    {
        'name': 'marklar', 
        'image_url': 'https://taco.pic/1', 
        'rating': 1, 
        'review_count': 2, 
        'distance': 3}]}


class TacoMeTest(unittest.TestCase):

    def test_commandtext_is_tacome(self):
        assert TacoMe().get_command() == "tacome"

    def test_available_in_all_channels(self):
        assert TacoMe().get_channel_id() == "all"

    def test_invoke_without_zip_returns_suggestion(self):
        result = TacoMe().invoke("tacome", "fake_user")
        assert result[0] == 'Try: `tacome _ZIP_CODE_`. Example: `tacome 90405`'

    @patch.object(TacoMe, 'get_data')
    def test_invoke_calls_get_data(self, get_data):
        get_data.return_value = {'total': 0}
        TacoMe().invoke(COMMAND, "fake_user")
        expected = "https://api.yelp.com/v3/businesses/search?term=taco&sort_by=distance&categories=foodtrucks&location=" + ZIP

        get_data.assert_called_with(expected)

    def test_create_slack_response_populates_attachment(self):
        actual = TacoMe().create_slack_response(API_RESPONSE_SAMPLE)
        for entry in ('title', 'image_url', 'text'):
            assert actual[1][0][entry]

    @patch.object(os.environ, 'get')
    def test_get_auth_value_returns_bearer(self,mock_get):
        mock_get.return_value = '<API KEY>'
        result = TacoMe().get_auth_value()
        assert result == 'Bearer <API KEY>'

    def test_get_zipcode_extracts_5digits(self):
        cases = {
            'tacome': None,
            'tacome 12345': '12345',
            'tacome   12345': '12345',
            'tacome   12345   ': '12345',
            'tacome 1234': None,
            'tacome 123456': None,
            'tacome a 123456': None
        }

        for command, expected in cases.iteritems():
            actual = TacoMe().get_zipcode(command)
            if (expected is None):
                assert actual is None
            else:
                assert actual == expected
