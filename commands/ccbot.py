import urllib
import json
import random

class CCBot:
    cats_url = "https://api.github.com/repos/flores/moarcats/contents/cats?ref=master"
    cats_cache = None

    def get_channel_id(self):
        return "all"

    def invoke(self, input):
        command,action,args= self.parse_command(input)
        return "ok you want me to " + action,None

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