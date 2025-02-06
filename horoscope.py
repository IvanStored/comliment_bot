import requests
import deepl
URL = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"


def get_horoscope_for_today() -> str:
    resp = requests.get(url=URL, params={"sign": "Sagittarius", "day": "TODAY"})
    data = resp.json()["data"]
    horoscope = data["horoscope_data"]
    return horoscope


def translate_horoscope_data(english_data: str, api_key: str) -> str:
    translator = deepl.Translator(auth_key=api_key)
    translated_data = translator.translate_text(english_data, target_lang="uk")
    return str(translated_data)
