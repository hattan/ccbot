# ccbot
SoCal Code Camp Slack bot

Commands are automaticatlly loaded at startup. To add a new command, add a class in the commands folder. The class must include
the following 3 method:

* get_channel_id(self):<Br/>
returns the channel ID where this command can execute. It can also be "all" for all public channels and private channels that ccbot is a member of.

* invoke(self, command, user)<Br/>
 This method gets called everytime someone invokes the command.
  
* get_command(self):<Br/>
Text used to invoke command. The input can contain other characters after the command text.
  
 
