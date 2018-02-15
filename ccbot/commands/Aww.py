from services.reddit_client import RedditApiClient

class Aww:
    url = "https://www.reddit.com/r/aww.json"
    reddit_client = None

    def get_channel_id(self):
        return "all"

    def invoke(self, command, user):
        if not self.reddit_client:
            self.reddit_client = RedditApiClient(self.url)

        attachments = self.reddit_client.fetch()
        return None,attachments

    def get_command(self):
        return "aww"

