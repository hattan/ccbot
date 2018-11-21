class HelpFactory:
    def __init__(self, commands):
        self.commands = commands

    def list(self):
        return self.commands.keys()

    def details(self, command_name):
        instance = self.commands.get(command_name)
        result = instance.__doc__ if instance is not None and instance.__doc__ is not None else command_name
        return result
    