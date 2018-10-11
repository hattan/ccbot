# encoding: utf-8
import random
import sys
import os

sys.path.append("ccbot")

from ccbot.commands.TacoMe import TacoMe
from ccbot.services.api_client import ApiClient
from ccbot.services.slack_response import SlackResponse
from mock import MagicMock, patch
import pytest
import unittest
from urllib2 import *

ZIP = '90405'
COMMAND = 'tacome ' + ZIP
API_RESPONSE_SAMPLE = {
    'total': 1,
    'businesses': [
        {
            'name': 'marklar',
            'image_url': 'https://taco.pic/1',
            'rating': 1,
            'review_count': 2,
            'distance': 3,
            'url': 'https://example.com/foo/bar'}]}


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
   
    @patch.object(TacoMe, 'get_data')
    def test_invoke_bad_url_error(self, get_data):
        get_data.side_effect = URLError('nope!')
        actual = TacoMe().invoke(COMMAND, "fake_user")
        assert actual == SlackResponse.text("('nope!',)")
        
    @patch.object(TacoMe, 'get_data')
    def test_invoke_bad_request_http_error(self, get_data):
        get_data.side_effect = HTTPError('fake_url',400, 'nope!',None,None)
        actual = TacoMe().invoke(COMMAND, "fake_user")
        assert actual == SlackResponse.text('HTTP Error 400: nope!')
        
    def test_create_slack_response_populates_attachment(self):
        actual = TacoMe().create_slack_response(API_RESPONSE_SAMPLE)
        for entry in ('title', 'image_url', 'text', 'author_link', 'author_name'):
            assert actual[1][0][entry]

    def test_create_slace_response_zero_results(self):
        actual = TacoMe().create_slack_response({'total':0})
        assert actual[0] == 'No taco ¯\\_(ツ)_/¯'

    @patch.object(os.environ, 'get')
    def test_get_auth_value_returns_bearer(self, mock_get):
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

    def test_get_data_calls_api(self):
        api_client = ApiClient()
        api_client.fetch = MagicMock(return_value='yup')

        target = TacoMe()
        target.api_client = api_client

        actual = target.get_data('dummy_url')

        assert actual == 'yup'
        target.api_client.fetch.assert_called_once()
