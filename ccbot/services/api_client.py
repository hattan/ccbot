import urllib2
import json

class ApiClient:
    user_agent = "codecamp-bot"

    def fetch(self,url,headers=None):
        resp = self.fetch_raw(url,headers)
        data = json.loads(resp)
        return data

    def fetch_raw(self,url,headers=None):
        req = urllib2.Request(url)
        req.add_header('User-Agent', self.user_agent)
        if headers is not None:
            for key in headers:
                req.add_header(key, headers[key])
        resp = urllib2.urlopen(req)
        data = resp.read()
        return data
