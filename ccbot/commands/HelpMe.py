import sys
sys.path.append("ccbot")

from services.BotCommand import BotCommand
from services.slack_response import SlackResponse
from services.help_factory import HelpFactory
from bot import commands


class HelpMe(BotCommand):
    def __init__(self):
        BotCommand.__init__(self, "helpme")

        self.commands = commands

    def invoke(self, command, user):
        parts = command.lower().split(' ')

        text = ''
        if len(parts) == 2:
            text = self.get_details(parts[1])
        else:
            text = self.get_listing()
        
        return SlackResponse.text(text = text)

    def get_listing(self):
        result = 'Command List:\n'
        for x in HelpFactory(self.commands).list():
            result += '* `%s`\n' % x

        return result

    def get_details(self, command_name):
        return '`%s`: %s' % (command_name, HelpFactory(self.commands).details(command_name))
