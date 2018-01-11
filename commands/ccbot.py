import datetime
import urllib2
import json
import random


class CCBot:
    cats_url = "https://api.github.com/repos/flores/moarcats/contents/cats?ref=master"
    cats_cache = None

    def get_channel_id(self):
        return "all"

    def invoke(self, input):
        text = None
        attachements = None
        command,action,args= self.parse_command(input)
        method_name = "action_" + action
        if method_name in dir(CCBot):
            method_to_call = getattr(self, method_name)
            result = method_to_call(args)
            text = result

        return text,attachements

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

    def action_schedule(self,args):
        return "https://www.socalcodecamp.com/schedule.aspx"

    def action_telljoke(self,args):
        req = urllib2.Request("https://icanhazdadjoke.com/")
        req.add_header('User-Agent', 'codecamp-bot')
        req.add_header('Accept','text/plain')
        resp = urllib2.urlopen(req)
        data = resp.read()
        return data
