import urllib2
import json
import random

class Xkcd:
   
    def get_channel_id(self):
        return "all"

    def fetch_info(self,comic_id = None):
        url = "https://xkcd.com/info.0.json" if comic_id is None else "https://xkcd.com/" + str(comic_id) + "/info.0.json"
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'codecamp-bot')
        req.add_header('Accept','text/plain')
        resp = urllib2.urlopen(req)
        data = json.loads(resp.read())
        return data

    def invoke(self, input, user):
        command,args= self.parse_command(input)
        comic_id = None
        if(len(args) > 0):
            comic_id = args[0]

        info = self.fetch_info()
        last_comic_id = info["num"]
        random_comic = comic_id if comic_id is not None else random.randint(0, last_comic_id)
        comic_data = self.fetch_info(random_comic)
        attachments = attachments = [{"title": comic_data["title"], "text": comic_data["alt"],"image_url":  comic_data["img"]}]
        return None,attachments

    def get_command(self):
        return "xkcd"

    def parse_command(self,command):
        parts = command.split(' ')
        size = len(parts)
        command = parts[0] if size > 0 else None
        count = 1
        args = []
        while(count<size):
            argument = parts[count].strip()
            if not argument is '':
                args.append(argument)
            count = count + 1
        return command,args

if __name__ == "__main__":
    xk = Xkcd()
    text,attachments = xk.invoke("xkcd 614" ,"user")
    print attachments
