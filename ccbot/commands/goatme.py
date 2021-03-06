import os
import random
from services.api_client import ApiClient
from services.slack_response import SlackResponse
from utils.cache import *

class GoatMe:
    url = "https://api.imgur.com/3/gallery/r/babygoats"
    imgur_key = os.environ.get('IMGUR_CLIENT_ID')
    api_client = None

    def __init__(self):
        self.api_client = ApiClient()

    def get_channel_id(self):
        return "all"
    
    @timed_memoize(minutes=30)
    def get_data(self):
        response = self.api_client.fetch(self.url, {'Authorization' : 'Client-ID ' + self.imgur_key})
        data = response.get("data",{})
        return [child['images'][0]['link'] if 'images' in child else child['link'] for child in data ]
        
    def invoke(self, command, user):
        data = self.get_data()
        image_url = random.choice(data)
        return SlackResponse.attachment(title=image_url,image_url=image_url)

    def get_command(self):
        return "goatme"

