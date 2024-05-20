from os import getenv

import requests
from dotenv import load_dotenv

load_dotenv()

CAT_TOKEN = getenv("TOKEN")
API_URL = "https://api.thecatapi.com/v1/images/search"
API_PARAMS = {"x-api-key": CAT_TOKEN}


def get_random_cat_image_url():
    response = requests.get(url=API_URL, params=API_PARAMS).json()
    image_url = response[0]["url"]
    return image_url
