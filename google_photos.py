import random

from gphotospy import authorize
from gphotospy.media import Media

CLIENT_SECRET_FILE = "client_secret.json"

service = authorize.init(CLIENT_SECRET_FILE)


def get_random_image_url() -> str:
    media_manager = Media(service)
    media_iterator = media_manager.list()
    photos = [image["baseUrl"] for image in media_iterator]
    return random.choice(photos)


if __name__ == '__main__':
    get_random_image_url()