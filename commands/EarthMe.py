import urllib2
import json
import random

class EarthMe:

    def get_info(self):
        url = "https://epic.gsfc.nasa.gov/api/images.php"
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'codecamp-bot')
        resp = urllib2.urlopen(req)
        data = json.loads(resp.read())
        image_data = data[0]
        return image_data

    def get_channel_id(self):
        return "all"

    def invoke(self, command, user):
        image_data = self.get_info()
        image_url = "https://epic.gsfc.nasa.gov/epic-archive/jpg/" + image_data['image'] + ".jpg"
        lat = str(image_data['centroid_coordinates']['lat'])
        lng = str(image_data['centroid_coordinates']['lon'])
        maps_url = "https://www.google.com/maps/@" + lat +  "," + lng + ",6z"
        pretext = image_data['caption']
        text = "Taken on " + image_data['date']
        author_name = lat + " " + lng + " (location map)"
        author_link = maps_url
        attachments = attachments = [{"pretext": pretext, "text":  text , "image_url": image_url, "author_name": author_name, "author_link": author_link}]
        return None,attachments

    def get_command(self):
        return "earthme"