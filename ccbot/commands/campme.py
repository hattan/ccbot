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
    USAGE_TEXT = 'Try: `campme next` or `campme now` or `campme speaker Bob Bobbernaugh`, or `campme sessions at 14:15` .'
    MANUAL = 'Help for the Code Camp Bot\n\n* `campme next` shows sessions starting next time slot.\n* `campme now` shows sessions in progress.\n* `campme speaker Marcel Marceau` shows sessions by the specified speakr. You may use first or last name only or both.\n* `campme sessions at 16:00` will return sessions starting at 4PM today. Use 24 hour clock 13:00 is 1PM, 14:00 is 2PM etc.'
    
    URL = "https://www.socalcodecamp.com/v1/schedule/sessions"

    def __init__(self):
        self.api_client = ApiClient()
        self.api_headers = {
            'Accept': 'application/json',
            'x-token': os.environ.get('SLACK_CODE_CAMP_BOT_CODECAMP_API_TOKEN')
        }

    def get_verb(self, command):
        parts = command.split()
        return parts[1:] if len(parts) > 1 else None

    @timed_memoize(minutes=30)
    def get_data(self, url):
        return self.api_client.fetch(url, headers=self.api_headers)

    def invoke(self, command, user):

        verb = self.get_verb(command)

        if(verb is None):
            return SlackResponse.text(self.USAGE_TEXT)

        if(verb[0] == 'help' or verb[0] == '?'):
            return SlackResponse.text(self.MANUAL)

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

        formatted = CampMe.format_text(subset, verb[0] == 'speaker')

        return SlackResponse.attachment(
            title=verb,
            text=formatted,
            author_name='Code Camp Bot',
            author_link='https://www.socalcodecamp.com/schedule.aspx')

    @staticmethod
    def filter_items(items, verb):
        if(verb[0] == 'now'):
            return [v for v in items if CampMe.is_now(v)]

        if(verb[0] == 'next'):
            return [v for v in items if CampMe.is_next(v)]

        if(verb[0] == 'speaker' and len(verb) > 1):
            regex = CampMe.build_regex(verb[1:])
            return [v for v in items if CampMe.is_by_speaker(v, regex)]
        
        if(verb[0] == 'sessions' and verb[1] == 'at' and len(verb) > 2):
            return [v for v in items if CampMe.is_at_time(v, verb[2], datetime.now() )]

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
        starts = datetime.strptime(session.get(
            'SessionStart'), "%Y-%m-%dT%H:%M:%S")
        now = datetime.now()
        return starts > now and starts < now + timedelta(hours=1, minutes=15)

    @staticmethod
    def build_regex(name_parts):
        pattern = '(\\b'
        pattern += '\\b|\\b'.join(name_parts)
        pattern += '\\b)'
        return re.compile(pattern, re.IGNORECASE)

    @staticmethod
    def is_by_speaker(session, regex):
        return (
            regex.search(session['SpeakerFirstName']) != None
            or regex.search(session['SpeakerLastName']) != None
        )
    
    @staticmethod
    def is_at_time(session, stated_time, clock):
        session_dt = datetime.strptime(session.get('SessionStart'),"%Y-%m-%dT%H:%M:%S")
        stated_dt = datetime.strptime(stated_time,"%H:%M")
        return (
            session_dt.hour == stated_dt.hour and
            session_dt.minute == stated_dt.minute and
            session_dt.day == clock.day
        )


    @staticmethod
    def nice(time_string):
        parsed = datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S")
        return parsed.strftime('%a %H:%M')

    @staticmethod
    def format_text(items, is_by_speaker = False):
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
            if (isfirst and not is_by_speaker):
                result += ('%s - %s\n================\n' % (
                    CampMe.nice(item.get('SessionStart')),
                    CampMe.nice(item.get('SessionEnd'))))
                isfirst = False

            result = result + ('*  %s %s: %s  @ %s %s\n' % (
                item.get('SpeakerFirstName'),
                item.get('SpeakerLastName'),
                item.get('SessionName'),
                item.get('Room'),
                CampMe.nice(item.get('SessionStart')) if is_by_speaker else ''
                ))

        return result

    def get_command(self):
        return "campme"

    def get_channel_id(self):
        return "all"
