import urllib
import json
import random

class CatMe:
    cats_url = "https://api.github.com/repos/flores/moarcats/contents/cats?ref=master"
    cats_cache = None

    def get_channel_id(self):
        return "all"

    def invoke(self, command, user):
        if self.cats_cache is None:
            response = urllib.urlopen(self.cats_url)
            data = json.loads(response.read())
            self.cats_cache = data
        image = random.choice(self.cats_cache)["name"]
        image_url = "http://edgecats.net/cats/" + image
        attachments = attachments = [{"title": image_url, "image_url": image_url}]
        return None,attachments

    def get_command(self):
        return "catme"