import random
from services.api_client import ApiClient

class EarthMe:
    api_client = None

    def __init__(self):
        self.api_client = ApiClient()

    def get_info(self):
        data = self.api_client.fetch("https://epic.gsfc.nasa.gov/api/images.php")
        image_data = random.choice(data)
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