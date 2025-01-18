import random

from gphotospy import authorize
from gphotospy.media import Media

CLIENT_SECRET_FILE = "client_secret.json"




def get_random_image_url() -> str:
    try:
        service = authorize.init(CLIENT_SECRET_FILE)
        media_manager = Media(service)
        media_iterator = media_manager.list()
        photos = [image["baseUrl"] for image in media_iterator]
        return random.choice(photos)
    except Exception as e:
        return ""


if __name__ == '__main__':
    get_random_image_url()