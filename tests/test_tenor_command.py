import random
import sys
sys.path.append("ccbot")

from ccbot.services.TenorCommand import TenorCommand
from ccbot.services.api_client import *
from ccbot.services.reddit_client import RedditApiClient
from services.slack_response import SlackResponse
from mock import MagicMock, patch

COMMAND_NAME = 'go_me'
SEARCH_TERM = 'dr. who'


def get_target():
    return TenorCommand(COMMAND_NAME, SEARCH_TERM)


def test_search_term():
    assert get_target().search_term == SEARCH_TERM


def test_url():
    assert TenorCommand.BASE_URL == 'https://api.tenor.com/v1/search?media_filter=minimal&q='


def test_get_search_url():
    assert get_target().get_search_url() == 'https://api.tenor.com/v1/search?media_filter=minimal&q=dr. who'

@patch.object(TenorCommand, 'get_data')
def test_invoke_with_no_data(get_data):
    get_data.retrun_value = None
    target = get_target()

    actual = target.invoke(None, None)

    assert actual[0] == 'No results for dr. who'

@patch.object(TenorCommand, 'get_data')
def test_invoke_with_zero_results(get_data):
    get_data.retrun_value = {'results': []}
    target = get_target()

    actual = target.invoke(None, None)

    assert actual[0] == 'No results for dr. who'
