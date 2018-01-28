import random
from services.api_client import ApiClient

class CatMe:
    cats_url = "https://api.github.com/repos/flores/moarcats/contents/cats?ref=master"
    api_client = None
    cats_cache = None

    def __init__(self):
        self.api_client = ApiClient()

    def get_channel_id(self):
        return "all"

    def invoke(self, command, user):
        if self.cats_cache is None:
            data = self.api_client.fetch(self.cats_url)
            self.cats_cache = data
        image = random.choice(self.cats_cache)["name"]
        image_url = "http://edgecats.net/cats/" + image
        attachments = attachments = [{"title": image_url, "image_url": image_url}]
        return None,attachments

    def get_command(self):
        return "catme"