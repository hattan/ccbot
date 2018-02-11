import random
from services.api_client import ApiClient
from services.slack_response import SlackResponse
from utils.cache import *

class CatMe:
    url = "https://api.github.com/repos/flores/moarcats/contents/cats?ref=master"
    api_client = None

    def __init__(self):
        self.api_client = ApiClient()

    def get_channel_id(self):
        return "all"

    @timed_memoize(minutes=30)
    def get_data(self):
        return self.api_client.fetch(self.url)

    def invoke(self, command, user):
        data = self.get_data()
        image = random.choice(data).get("name","")
        image_url = "http://edgecats.net/cats/" + image
        return SlackResponse.attachment(title=image_url,image_url= image_url)

    def get_command(self):
        return "catme"