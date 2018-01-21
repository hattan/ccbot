import urllib2
import json
import random

class TortoiseMe:
    url = "https://www.reddit.com/r/tortoise.json"
    cache = []
    def get_channel_id(self):
        return "all"

    def invoke(self, command, user):
        if not self.cache:
            req = urllib2.Request(self.url)
            req.add_header('User-Agent', 'codecamp-bot')
            resp = urllib2.urlopen(req)
            data = json.loads(resp.read())
            for child in data['data']['children']:
                if 'preview' in child['data']:
                    images = child['data']['preview']['images']
                    self.cache.append(images[0]['source']['url'])
        image_url = random.choice(self.cache)
        attachments = attachments = [{"title": image_url, "image_url": image_url}]
        return None,attachments

    def get_command(self):
        return "tortoiseme"

