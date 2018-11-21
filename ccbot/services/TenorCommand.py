import os
import random
from BotCommand import BotCommand
from services.api_client import ApiClient
from services.slack_response import SlackResponse
from utils.cache import *

        

class TenorCommand(BotCommand):
    BASE_URL = 'https://api.tenor.com/v1/search?media_filter=minimal&q='
    api_client = None

    def __init__(self, command_name, search_term):
        """ Creates a Tenor ccbot command named command_name

        Args:
            command_name: The command name. This will be the utterance invoking the command.
            search_term: The text to search against the Tenor web service. Note that you should 
                url encode any spaces or special characters. For example 'dr.+who' not 'dr. who'
        """

        BotCommand.__init__(self, command_name, 'all')
        self.search_term = search_term
        self.api_client = ApiClient()

    def get_data(self):
        return self.api_client.fetch(self.get_search_url() , {'Content-Type': 'application/json', 'Accept': 'application/json'})

    def get_search_url(self):
        return self.BASE_URL + self.search_term

    def invoke(self, command, user):
        data = self.get_data()

        if data is None or data['results'] is None or len(data['results']) < 1:
            return SlackResponse.text('No results for ' + self.search_term)

        item = random.choice(data['results'])

        return TenorCommand.create_slack_response(item)

    @staticmethod
    def create_slack_response(item):
        return SlackResponse.attachment(title='Here you go:',
                                 image_url=item['media'][0]['gif']['url'],
                                 author_link=item['url'],
                                 author_name='Via Tenor'
                                 )



