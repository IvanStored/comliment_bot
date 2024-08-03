import requests
from deep_translator import GoogleTranslator
URL = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"


def get_horoscope_for_today() -> str:
    resp = requests.get(url=URL, params={"sign": "Sagittarius", "day": "TODAY"})
    data = resp.json()["data"]
    horoscope = data["horoscope_data"]
    return horoscope


def translate_horoscope_data(english_data: str) -> str:
    translator = GoogleTranslator(source="auto", target="uk")
    translated_data = translator.translate(english_data)
    return translated_data

