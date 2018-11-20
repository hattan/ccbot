class BotCommand(object):
    def __init__(self, command_name, channel_id="all"):
        """ Creates a BotCommand

        Args:
            command_name: The command name. This will be the utterance invoking the command.
            channel_id: The name of the channel to register this bot to. Use the special constant 'all' to allow bot in all channels'
        """

        self.command_name = command_name.lower()
        
        self.channel_id = channel_id

    def get_command(self):
        return self.command_name
    
    def get_channel_id(self):
        return self.channel_id
