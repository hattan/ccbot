import datetime
import random
import os
import bot
from services.api_client import ApiClient
from services.slack_response import SlackResponse

class CCBot:
    deny_response = [
        'No, {name}. I won''t {action}. I REFUSE',
        'Oh boy, here we go again. Why don''t you like me {name}? {action}? really .. REALLY?',
        'Doesn''t this get old, {name}? Would you rather I give you a computer error? Fine.... {action} is not supported. Go Away',
        'What did I ever do to you {name}? Do I deserve this torment? I''m just a friendly bot and you ask me unspeakable things like {action}',
        'JUST ... STOP, {name}. URGH..{action}, really?'
    ]
    bully_id = os.environ.get('BULLY_USER_ID')
    bully_name = None
    api_client = None

    def __init__(self):
        self.api_client = ApiClient()
        
    def get_channel_id(self):
        return "all"

    def invoke(self, input, user):
        self.bully_name = bot.get_user_name_by_id(self.bully_id)
        text = None
        command,action,args= self.parse_command(input)
        method_name = "action_" + action
        if method_name in dir(self):
            method_to_call = getattr(self, method_name)
            result = method_to_call(args)
            text = result
        else:
            if user == self.bully_id:
                result = random.choice(self.deny_response).format(name=self.bully_name, action=action)
                text = result

        return SlackResponse.text(text)

    def get_command(self):
        return "ccbot"

    def parse_command(self,command):
        parts = command.split(' ')
        size = len(parts)
        command = parts[0] if size > 0 else None
        action = parts[1] if size > 1 else None
        count = 2
        args = []
        while(count<size):
            argument = parts[count].strip()
            if not argument is '':
                args.append(argument)
            count = count + 1
        return command,action,args

#CCBot actions in the format "ccbot <action> <args>"
#All actions receive an args array with any data passed in
    def action_get_time(self,args):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def action_schedule(self,args=[]):
        return "https://www.socalcodecamp.com/schedule.aspx"

    def action_telljoke(self,args):
        headers = {'Accept' : 'text/plain'}
        data = self.api_client.fetch_raw("https://icanhazdadjoke.com/",headers)
        return data

    def action_debug_bully_id(self,args=[]):
        return self.bully_id

    def action_debug_bully_name(self,args=[]):
        return self.bully_name