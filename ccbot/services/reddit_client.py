import random

from api_client import ApiClient
from utils.cache import memoize
from slack_response import SlackResponse

class RedditApiClient(ApiClient):

    def __init__(self, url='', use_cache=True):
        self.url = url

    @memoize
    def get_data(self):
        result = []
        response = ApiClient.fetch(self,self.url)
        data = response.get("data",{})
        children = data.get("children",{})
        return [child['data']['preview']['images'][0]['source']['url'] for child in children if 'preview' in child.get("data",{})]

    def fetch(self):
        data = self.get_data()
        image_url = random.choice(data)
        text,attachment = SlackResponse.attachment(title=image_url,image_url=image_url)
        return attachment






