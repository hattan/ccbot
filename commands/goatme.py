import os
import urllib2
import json
import random

class GoatMe:
    url = "https://api.imgur.com/3/gallery/r/babygoats"
    imgur_key = os.environ.get('IMGUR_CLIENT_ID')
    cache = []
    def get_channel_id(self):
        return "all"

    def invoke(self, command, user):
        if not self.cache:
            req = urllib2.Request(self.url)
            req.add_header('User-Agent', 'codecamp-bot')
            req.add_header('Authorization','Client-ID ' + self.imgur_key)
            resp = urllib2.urlopen(req)
            data = json.loads(resp.read())
            for child in data['data']:
                if 'images' in child:
                    self.cache.append(child['images'][0]['link'])
                else:
                     self.cache.append(child['link'])
        image_url = random.choice(self.cache)
        attachments = attachments = [{"title": image_url, "image_url": image_url}]
        return None,attachments

    def get_command(self):
        return "goatme"

