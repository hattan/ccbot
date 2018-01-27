from api_client import ApiClient
import random

class RedditApiClient(ApiClient):
    use_cache = None
    cache = []
    def __init__(self, url, use_cache=True):
        self.use_cache = use_cache
        self.url = url

    def get_data(self):
        result = []
        data = ApiClient.fetch(self,self.url)
        for child in data['data']['children']:
            if 'preview' in child['data']:
                images = child['data']['preview']['images']
                result.append(images[0]['source']['url'])
        return result

    def fetch(self):
        if self.use_cache:
            if len(self.cache) == 0:
                self.cache = self.get_data()
            data = self.cache
        else:
            data = self.get_data()

        image_url = random.choice(data)
        attachments = attachments = [{"title": image_url, "image_url": image_url}]
        return attachments
   

if __name__ == "__main__":
    client = RedditApiClient("https://www.reddit.com/r/aww.json",use_cache=True)
    attachment = client.fetch()
    print attachment






