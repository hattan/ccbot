from commands.dogme import DogMe

def test_dogme_commandtext_is_dogme():
    dogme = DogMe()
    command_text = dogme.get_command()
    assert command_text == "dogme"

def test_dogme_available_in_all_channels():
    dogme = DogMe()
    channel = dogme.get_channel_id()
    assert channel == "all"