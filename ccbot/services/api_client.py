import urllib2
import json

class ApiClient:
    user_agent = "codecamp-bot"

    def fetch(self,url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', self.user_agent)
        resp = urllib2.urlopen(req)
        data = json.loads(resp.read())
        return data
