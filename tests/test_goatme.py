import uuid
import sys
sys.path.append("ccbot")

from ccbot.commands.goatme import GoatMe
from services.api_client import ApiClient
from utils.cache import *
from mock_datetime import mock_datetime 
from mock import MagicMock,patch

def test_goatme_url_is_imgur_babbygoats():
    assert GoatMe().url == "https://api.imgur.com/3/gallery/r/babygoats"
    
def test_goatme_commandtext_is_dogme():
    assert GoatMe().get_command() == "goatme"

def test_goatme_available_in_all_channels():
    assert GoatMe().get_channel_id() == "all"

def test_goatme_invoke_calls_api_client_fetch_returns_url_from_link_if_no_images_array():
    api_client = ApiClient()
    api_client.fetch = MagicMock(return_value={'data':[{'link':'test_url'}]})
    goat_me = GoatMe()
    goat_me.imgur_key = "fake_imgur_key"
    goat_me.api_client=api_client
    text,attachments = goat_me.invoke("goatme","fakeuser")
    assert attachments == [{'image_url': 'test_url', 'title': 'test_url'}]  

def test_goatme_invoke_calls_api_client_fetch_returns_url_from_images_array_if_images_array_exists():
    api_client = ApiClient()
    api_client.fetch = MagicMock(return_value={'data':[{'link':'test_url','images' : [{'link':'test_url_2'}]}]})
    goat_me = GoatMe()
    goat_me.imgur_key = "fake_imgur_key"
    goat_me.api_client=api_client
    text,attachments = goat_me.invoke("goatme","fakeuser")
    assert attachments == [{'image_url': 'test_url_2', 'title': 'test_url_2'}]

def test_goatme_invoke_caches_api_client_fetch_if_less_than_30_minutes():
    #arrange
    id = uuid.uuid1()
    api_client = ApiClient()
    api_client.fetch = MagicMock(return_value={'data':[{'link':id}]})
    goat_me = GoatMe()
    goat_me.imgur_key = "fake_imgur_key"
    goat_me.api_client=api_client

    #act
    text,attachments = goat_me.invoke("goatme","fakeuser")
    
    #assert
    assert attachments == [{'image_url': id, 'title': id}]

    target = datetime.datetime.now() + datetime.timedelta(minutes=12) #change datetime to 12 minutes from now
    with mock_datetime(target, datetime):     
        api_client.fetch = MagicMock(return_value={'data':[{'link':uuid.uuid1()}]})
        text,attachments = goat_me.invoke("goatme","fakeuser")
        assert attachments == [{'image_url': id, 'title': id}]

def test_goatme_invoke_calls_api_client_fetch_if_greater_than_30_minutes():
    #arrange
    id = uuid.uuid1()
    api_client = ApiClient()
    api_client.fetch = MagicMock(return_value={'data':[{'link':id}]})
    goat_me = GoatMe()
    goat_me.imgur_key = "fake_imgur_key"
    goat_me.api_client=api_client

    #act
    text,attachments = goat_me.invoke("goatme","fakeuser")
    
    #assert
    assert attachments == [{'image_url': id, 'title': id}]

    target = datetime.datetime.now() + datetime.timedelta(minutes=40) #change datetime to 12 minutes from now
    with mock_datetime(target, datetime):     
        new_id = uuid.uuid1()
        api_client.fetch = MagicMock(return_value={'data':[{'link':new_id}]})
        text,attachments = goat_me.invoke("goatme","fakeuser")
        assert attachments != [{'image_url': id, 'title': id}]
        assert attachments == [{'image_url': new_id, 'title': new_id}]


