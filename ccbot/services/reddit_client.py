import random

from api_client import ApiClient
from utils.cache import memoize


class RedditApiClient(ApiClient):

    def __init__(self, url='', use_cache=True):
        self.url = url

    @memoize
    def get_data(self):
        result = []
        data = ApiClient.fetch(self,self.url)
        for child in data['data']['children']:
            if 'preview' in child['data']:
                images = child['data']['preview']['images']
                result.append(images[0]['source']['url'])
        return result

    def fetch(self):
        data = self.get_data()
        image_url = random.choice(data)
        attachments = attachments = [{"title": image_url, "image_url": image_url}]
        return attachments






