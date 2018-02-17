#!/usr/bin/env python

import os
import glob
import importlib
import inspect
import time
from slackclient import SlackClient

commands = {}
slack_client = SlackClient(os.environ.get('SLACK_CODE_CAMP_BOT_TOKEN'))
users = None

def get_user_name_by_id(id):
    global users
    return [user["profile"]["display_name"] for user in users.get("members",{}) if user["id"] == id][0]

def is_command(handler_class):
    return handler_class and inspect.isclass(handler_class) and str(handler_class).startswith("commands.")

def get_class(module,member):
    return getattr(module, member)

def load_commands():
    current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    for file in glob.glob(current_dir + "/commands/*.py"):
        name = os.path.splitext(os.path.basename(file))[0]
 
        if name.startswith("__"):
            continue

        module = importlib.import_module("." + name,package="commands")

        for member in dir(module):
            handler_class = get_class(module,member)

            if is_command(handler_class):
                commands[handler_class().get_command()]=handler_class()
                
def handle_command(input, channel, user):
    if not input is '':
        parts = input.split(' ')
        command = parts[0].lower()
        if command in commands:
            action = commands[command]
            actionChannel = action.get_channel_id()

            if (actionChannel == "all") or (channel == action.get_channel_id()):
                text,attachments = action.invoke(input,user)
                if text is not None:
                    slack_client.api_call("chat.postMessage", channel=channel,text=text, as_user=True)
                else:
                    slack_client.api_call("chat.postMessage", channel=channel,
                        text="",
                        attachments=attachments, as_user=True)

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                return output['text'].strip(), output['channel'], output['user']

    return None, None, None

def running():
    return True

def get_sleep_time():
    return 1 #second delay between reading from firehose

def start_bot():
    global users
    users = slack_client.api_call("users.list")
    bot_id = slack_client.api_call("auth.test")["user_id"]
    bot_name = get_user_name_by_id(bot_id)

    load_commands()

    READ_WEBSOCKET_DELAY = get_sleep_time()
    if slack_client.rtm_connect():
        print(bot_name + " connected and running!")
        while running():
            command, channel, user = parse_slack_output(slack_client.rtm_read())
           
            if command and channel:
                handle_command(command, channel, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

   
