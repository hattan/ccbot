import random
from services.api_client import ApiClient
from services.slack_response import SlackResponse

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

    def get_data(self):
        image_data = self.get_info()
        return (image_data.get('image',None) , 
                str(image_data['centroid_coordinates']['lat']), 
                str(image_data['centroid_coordinates']['lon']),
                image_data['caption'],
                image_data['date'])

    def invoke(self, command, user):
        image, lat, lng , caption, date = self.get_data()
        image_url = "https://epic.gsfc.nasa.gov/epic-archive/jpg/" + image + ".jpg"
        maps_url = "https://www.google.com/maps/@" + lat +  "," + lng + ",6z"
        pretext = caption
        text = "Taken on " + date
        author_name = lat + " " + lng + " (location map)"
        author_link = maps_url
        return SlackResponse.attachment(pretext=pretext,text=text,image_url=image_url,author_name=author_name,author_link=author_link)

    def get_command(self):
        return "earthme"