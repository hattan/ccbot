# encoding: utf-8
import re
import os
from services.api_client import ApiClient
from services.slack_response import SlackResponse
from utils.cache import *
from urllib2 import *

class TacoMe:
    url = "https://api.yelp.com/v3/businesses/search?term=taco&sort_by=distance&categories=foodtrucks&location="
    api_client = None

    def __init__(self):
        self.api_client = ApiClient()
        self.api_headers = {
            'Accept': 'application/json',
            'Authorization': self.get_auth_value()
        }
        self.zipcode_re = re.compile(r'^tacome\s+(\d{5})\s*$')

    def get_channel_id(self):
        return "all"

    def get_auth_value(self):
        token = os.environ.get('SLACK_CODE_CAMP_BOT_YELP_TOKEN')
        return 'Bearer ' + token if token else None

    def get_zipcode(self, command):
        matched = self.zipcode_re.match(command)
        return matched.group(1) if matched else None

    def get_data(self, url):
        return self.api_client.fetch(url, headers=self.api_headers)

    def invoke(self, command, user):

        zip = self.get_zipcode(command)

        if(zip is None):
            return SlackResponse.text(r'Try: `tacome _ZIP_CODE_`. Example: `tacome 90405`')

        url = self.url+zip
        
        try:
            result = self.get_data(url)
        except HTTPError as he:
            return SlackResponse.text(str(he))
        except URLError as ue:
            return SlackResponse.text(str(ue.args))

        return self.create_slack_response(result)

    def create_slack_response(self, api_response):
        if (api_response['total'] == 0):
            return SlackResponse.text('No taco ¯\\_(ツ)_/¯')

        found = random.choice(api_response['businesses'])
        
        description = 'Rated %s by %s people, is %s meters away' % (
            found['rating'],
            found['review_count'],
            int(found['distance'])
            )

        return SlackResponse.attachment(
            title=found['name'],
            image_url=found['image_url'],
            text=description,
            author_name='Taco details...',
            author_link=found['url'])

    def get_command(self):
        return "tacome"
