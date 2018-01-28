import urllib2
import json
import random

from services.reddit_client import RedditApiClient

class DogMe():
    url = "https://www.reddit.com/r/puppies.json"
    
    def get_channel_id(self):
        return "all"

    def invoke(self, command, user):
        reddit_client = RedditApiClient(self.url)
        attachments = reddit_client.fetch()
        return None,attachments

    def get_command(self):
        return "dogme"

