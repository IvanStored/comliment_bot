from settings import Settings

import requests
import deepl


def get_horoscope_for_today() -> str:
    resp = requests.get(url=Settings.HOROSCOPE_URL, params={'sign': 'Sagittarius', 'day': 'TODAY'})
    data = resp.json()['data']
    horoscope = data['horoscope_data']
    return horoscope


def translate_horoscope_data(english_data: str, api_key: str) -> str:
    translator = deepl.Translator(auth_key=api_key)
    translated_data = translator.translate_text(english_data, target_lang='uk')
    return str(translated_data)


def get_random_cat_image_url():
    response = requests.get(url=Settings.API_URL, params=Settings.API_PARAMS).json()
    image_url = response[0]['url']
    return image_url
