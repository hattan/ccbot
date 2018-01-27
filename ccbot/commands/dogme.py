
import urllib2
import json
import random

class DogMe:
    dogs_url = "https://www.reddit.com/r/puppies.json"
    dogs_cache = []
    def get_channel_id(self):
        return "all"

    def invoke(self, command, user):
        if not self.dogs_cache:
            req = urllib2.Request(self.dogs_url)
            req.add_header('User-Agent', 'codecamp-bot')
            resp = urllib2.urlopen(req)
            data = json.loads(resp.read())
            for child in data['data']['children']:
                if 'preview' in child['data']:
                    images = child['data']['preview']['images']
                    self.dogs_cache.append(images[0]['source']['url'])
        image_url = random.choice(self.dogs_cache)
        attachments = attachments = [{"title": image_url, "image_url": image_url}]
        return None,attachments

    def get_command(self):
        return "dogme"

if __name__ == "__main__":
    dogme = DogMe()
    text,attachments = dogme.invoke()
    print attachments