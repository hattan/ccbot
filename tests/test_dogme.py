from ccbot.commands.dogme import DogMe


from mock import MagicMock

def test_dogme_url_is_puppies_subreddit():
    dogme = DogMe()
    assert dogme.url == "https://www.reddit.com/r/puppies.json"
    
