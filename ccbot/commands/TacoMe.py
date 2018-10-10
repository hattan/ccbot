import os
from services.api_client import ApiClient
from services.slack_response import SlackResponse
from utils.cache import *
from urllib2 import *


class TacoMe:
    url = "https://api.yelp.com/v3/businesses/search?term=taco&sort_by=distance&categories=foodtrucks&location=90405"
    api_client = None

    def __init__(self):
        self.api_client = ApiClient()
        self.api_headers = {
            'Accept': 'application/json',
            'Authorization': self.get_auth_value()
        }

    def get_channel_id(self):
        return "all"

    def get_auth_value(self):
        token = os.environ.get('SLACK_CODE_CAMP_BOT_YELP_TOKEN')
        return 'Bearer ' + token if token else None

    def get_data(self):
        return self.api_client.fetch(self.url, headers=self.api_headers)

    def invoke(self, command, user):
        try:
            result = self.get_data()
        except HTTPError as he:
            return SlackResponse.text(str(he))
        except URLError as ue:
            return SlackResponse.text(str(e.args))

        if (result['total'] == 0):
            return SlackResponse.text('Sorry, no taco for ' + command)

        found = result['businesses'][0]
        description = 'Rated %s by %s people, is %s meters away price level %s' % (
            found['rating'], found['review_count'], found['distance'], found['price'])
        return SlackResponse.attachment(
            title=found['name'],
            image_url=found['image_url'],
            text=description)

    def get_command(self):
        return "tacome"
