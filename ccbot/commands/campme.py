# encoding: utf-8
import re
import os
import random
from services.api_client import ApiClient
from services.slack_response import SlackResponse
from utils.cache import timed_memoize
from urllib2 import HTTPError, URLError
from datetime import date, datetime, timedelta



class CampMe:
    api_client = None
    USAGE_TEXT = 'Try: `campme next` or `campme now`.'
    URL = "https://www.socalcodecamp.com/v1/schedule/sessions"
    def __init__(self):
        self.api_client = ApiClient()
        self.api_headers = {
            'Accept': 'application/json',
            'x-token': os.environ.get('SLACK_CODE_CAMP_BOT_CODECAMP_API_TOKEN')
        }
        self.verb_regex = re.compile(r'^campme\s+(\w+)\s*$')

    def get_verb(self, command):
        matched = self.verb_regex.match(command)
        return matched.group(1) if matched else None

    @timed_memoize(minutes=30)
    def get_data(self, url):
        return self.api_client.fetch(url, headers=self.api_headers)

    def invoke(self, command, user):

        verb = self.get_verb(command)

        if(verb is None):
            return SlackResponse.text(self.USAGE_TEXT)

        try:
            result = self.get_data(self.URL)
        except HTTPError as he:
            return SlackResponse.text(str(he))
        except URLError as ue:
            return SlackResponse.text(str(ue.args))

        return self.create_slack_response(result, verb)

    @staticmethod
    def create_slack_response(api_response, verb):
        if (len(api_response) == 0):
            return SlackResponse.text('Server returned no data ¯\\_(ツ)_/¯')

        subset = CampMe.filter_items(api_response, verb)

        formatted = CampMe.format_text(subset)

        return SlackResponse.attachment(
            title=verb,
            text=formatted,
            author_name='Code Camp Bot',
            author_link='https://www.socalcodecamp.com/schedule.aspx')

    @staticmethod
    def filter_items(items, verb):
        if(verb == 'now'):
            return [v for v in items if CampMe.is_now(v)]

        if(verb == 'next'):
            return [v for v in items if CampMe.is_next(v)]

        return items

    @staticmethod
    def is_now(session):
        starts = datetime.strptime(session.get(
            'SessionStart'), "%Y-%m-%dT%H:%M:%S")
        ends = datetime.strptime(session.get(
            'SessionEnd'), "%Y-%m-%dT%H:%M:%S")
        now = datetime.now()
        return now >= starts and now < ends

    @staticmethod
    def is_next(session):
        starts = datetime.strptime(session.get('SessionStart'), "%Y-%m-%dT%H:%M:%S")
        now = datetime.now()
        return starts > now and starts < now + timedelta(hours=1, minutes=15)

    @staticmethod 
    def nice(time_string):
        parsed = datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S")
        return parsed.strftime('%a %H:%M')

    @staticmethod
    def format_text(items):
        result = ''

        # u'Room' (98644544):u'SLH 102'
        # u'SessionEnd' (98644880):u'2018-11-11T11:15:00'
        # u'SessionId' (98644352):u'a83dca4a-06f8-48b6-a398-e857c74d6a30'
        # u'SessionName' (96970048):u'How to Ace Technical Interviews'
        # u'SessionStart' (98644304):u'2018-11-11T10:15:00'
        # u'SpeakerFirstName' (98639808):u'Abhi'
        # u'SpeakerLastName' (98639664):u'Jain'
        isfirst = True

        for item in items:
            if isfirst:
                result += ('%s - %s\n================\n' %(
                    CampMe.nice(item.get('SessionStart')),
                    CampMe.nice(item.get('SessionEnd'))))
                isfirst = False 
        
            result = result + ('*  %s %s: %s  @  %s\n' % (
                item.get('SpeakerFirstName'),
                item.get('SpeakerLastName'),
                item.get('SessionName'),
                item.get('Room')))

        return result

    def get_command(self):
        return "campme"

    def get_channel_id(self):
        return "all"
