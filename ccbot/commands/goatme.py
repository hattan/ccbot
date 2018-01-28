import os
import random
from services.api_client import ApiClient
from services.slack_response import SlackResponse

class GoatMe:
    url = "https://api.imgur.com/3/gallery/r/babygoats"
    imgur_key = os.environ.get('IMGUR_CLIENT_ID')
    cache = []
    api_client = None

    def __init__(self):
        self.api_client = ApiClient()

    def get_channel_id(self):
        return "all"

    def invoke(self, command, user):
        if not self.cache:
            headers = {'Authorization' : 'Client-ID ' + self.imgur_key}
            data = self.api_client.fetch(self.url,headers)
            for child in data['data']:
                if 'images' in child:
                    self.cache.append(child['images'][0]['link'])
                else:
                     self.cache.append(child['link'])

        image_url = random.choice(self.cache)
        
        return SlackResponse.attachment(title=image_url,image_url=image_url)

    def get_command(self):
        return "goatme"

