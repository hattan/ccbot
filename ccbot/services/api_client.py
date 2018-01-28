import urllib2
import json

class ApiClient:
    user_agent = "codecamp-bot"

    def fetch(self,url):
        resp = self.fetch_raw(url)
        data = json.loads(resp)
        return data

    def fetch_raw(self,url,accept=None):
        req = urllib2.Request(url)
        req.add_header('User-Agent', self.user_agent)
        if accept is not None:
            req.add_header('Accept',accept)
            
        resp = urllib2.urlopen(req)
        data = resp.read()
        return data
