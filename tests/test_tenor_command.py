import random
import sys
sys.path.append("ccbot")

from ccbot.services.TenorCommand import TenorCommand
from ccbot.services.api_client import *
from ccbot.services.reddit_client import RedditApiClient
from services.slack_response import SlackResponse
import pytest
import unittest
from mock import MagicMock, patch

COMMAND_NAME = 'go_me'
SEARCH_TERM = 'dr. who'
SAMPLE_RESULT = {'url': 'yo1', 'media': [{'gif': {'url': 'yo2'}}]}


def get_target():
    return TenorCommand(COMMAND_NAME, SEARCH_TERM)


class CampMeTest(unittest.TestCase):

    def test_search_term(self):
        assert get_target().search_term == SEARCH_TERM


    def test_url(self):
        assert TenorCommand.BASE_URL == 'https://api.tenor.com/v1/search?media_filter=minimal&q='


    def test_get_search_url(self):
        assert get_target().get_search_url(
        ) == 'https://api.tenor.com/v1/search?media_filter=minimal&q=dr. who'


    @patch.object(TenorCommand, 'get_data')
    def test_invoke_with_no_data(self,get_data):
        get_data.return_value = None
        target = get_target()

        text, attachments = target.invoke(None, None)

        assert text == 'No results for dr. who'


    @patch.object(TenorCommand, 'get_data')
    def test_invoke_with_zero_results(self, get_data):
        get_data.return_value = {'results': []}
        target = get_target()

        text, attachments = target.invoke(None, None)

        assert text == 'No results for dr. who'


    @patch.object(TenorCommand, 'get_data')
    def test_invoke_returning_data(self, get_data):
        get_data.return_value = {'results': [SAMPLE_RESULT]}

        target = get_target()

        text, attachments = target.invoke(None, None)

        assert attachments


    def test_get_data(self):
        api_client = ApiClient()
        api_client.fetch = MagicMock(return_value='yes')
        target = get_target()
        target.api_client = api_client
        actual = target.get_data()
        assert actual == 'yes'


    def test_create_slack_response_has_url(self):
        text, attachments = TenorCommand.create_slack_response(SAMPLE_RESULT)
        assert attachments[0]['author_link'] == 'yo1'


    def test_create_slack_response_has_gif_url(self):
        text, attachments = TenorCommand.create_slack_response(SAMPLE_RESULT)
        assert attachments[0]['image_url'] == 'yo2'
