class BotCommand(object):
    def __init__(self, command_name, channel_id="all"):
        self.command_name = command_name
        self.channel_id = channel_id

    def get_command(self):
        return self.command_name
    
    def get_channel_id(self):
        return self.channel_id
