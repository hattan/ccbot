from services.reddit_client import RedditApiClient

class DogMe():
    url = "https://www.reddit.com/r/puppies.json"
    reddit_client = None

    def get_channel_id(self):
        return "all"

    def configure_api_client(self):
        if self.reddit_client is None:
            self.reddit_client = RedditApiClient(self.url)

    def fetch_data(self):
        return self.reddit_client.fetch()

    def invoke(self, command, user):
        self.configure_api_client()
        attachments = self.fetch_data()
        return None,attachments
        
    def get_command(self):
        return "dogme"