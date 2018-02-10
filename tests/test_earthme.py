import random
import sys
sys.path.append("ccbot")

from ccbot.commands.EarthMe import EarthMe
from ccbot.services.api_client import *
from ccbot.services.reddit_client import RedditApiClient
from services.slack_response import SlackResponse
from mock import MagicMock,patch

def test_commandtext_is_xkcd():
    assert EarthMe().get_command() == "earthme"

def test_available_in_all_channels():
    assert EarthMe().get_channel_id() == "all"

def test_get_info_calls_nasa_api():
    #arrange
    api_client = ApiClient()
    api_client.fetch = MagicMock(return_value = [1])
    e = EarthMe()
    e.api_client = api_client
    #act
    e.get_info()
    #assert
    api_client.fetch.assert_called_with("https://epic.gsfc.nasa.gov/api/images.php")

@patch('random.choice')
def test_get_info_calls_nasa_api_returns_item_in_list(fake_choice):
    #arrange
    api_client = ApiClient()
    api_client.fetch = MagicMock(return_value = [1,2,3])
    e = EarthMe()
    e.api_client = api_client
    #act
    result = e.get_info()
    #assert
    fake_choice.assert_called_with([1,2,3])

def test_invoke():
    #arrange
    e = EarthMe()
    e.get_info = MagicMock(return_value = {'image' : 'fake_img','centroid_coordinates' : {'lat' : 1, 'lon' : 2} , 'caption' : 'captionit','date' : '1/1/1111'})
    #act
    result = e.invoke("earthme","fake_user")
    #assert
    assert result == SlackResponse.attachment(pretext='captionit',text="Taken on 1/1/1111",image_url="https://epic.gsfc.nasa.gov/epic-archive/jpg/fake_img.jpg",author_name="1 2 (location map)",author_link='https://www.google.com/maps/@1,2,6z')



