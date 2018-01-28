from services.reddit_client import RedditApiClient

class DogMe():
    url = "https://www.reddit.com/r/puppies.json"
    reddit_client = None

    def get_channel_id(self):
        return "all"

    def invoke(self, command, user):
        if self.reddit_client is None:
            self.reddit_client = RedditApiClient(self.url)

        attachments = self.reddit_client.fetch()
        return None,attachments
        

    def get_command(self):
        return "dogme"

