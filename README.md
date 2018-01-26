# ccbot
SoCal Code Camp Slack bot

### Adding new Commands 
Installation:

In order to use ccbot with slack, you need to create a [slack app](https://api.slack.com/apps?new_app=1). After creating an app, you need to get you API Token. That token needs to be added to an environment variable named 'SLACK_CODE_CAMP_BOT_TOKEN'

Install deps : 

    pip install -r requirements.text 

Start bot:

    ccbot/bot
    
The bot should be up and running.

Note: If you would like the bot to work in private channels, you need to invite the bot to the channel.
  
### Adding new Commands
Commands are automaticatlly loaded at startup. To add a new command, add a class in the commands folder. The class must include
the following 3 method:

* get_channel_id(self):<Br/>
returns the channel ID where this command can execute. It can also be "all" for all public channels and private channels that ccbot is a member of.

* invoke(self, command, user)<Br/>
 This method gets called everytime someone invokes the command.
  
* get_command(self):<Br/>
Text used to invoke command. The input can contain other characters after the command text.
  
 
