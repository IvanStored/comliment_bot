from os import getenv

import requests
from dotenv import load_dotenv

from horoscope import translate_horoscope_data, get_horoscope_for_today

load_dotenv()
TOKEN = getenv("TOKEN")
ADMIN_USER_ID = int(getenv("ADMIN_USER_ID"))
RECEIVER_USER_ID = int(getenv("RECEIVER_USER_ID"))
DEEPL_API = getenv("DEEPL_API")
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send_message() -> None:
    horoscope = translate_horoscope_data(english_data=get_horoscope_for_today(), api_key=DEEPL_API)
    requests.post(url=url, data={"chat_id": RECEIVER_USER_ID, "text": horoscope})


if __name__ == '__main__':
    send_message()
