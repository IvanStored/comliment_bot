from os import getenv

import requests
from dotenv import load_dotenv

from horoscope import translate_horoscope_data, get_horoscope_for_today

load_dotenv()
TOKEN = getenv("TOKEN")
ADMIN_USER_ID = int(getenv("ADMIN_USER_ID"))
RECEIVER_USER_ID = int(getenv("RECEIVER_USER_ID"))
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send_message() -> None:
    horoscope = get_horoscope_for_today()
    requests.post(url=url, data={"chat_id": ADMIN_USER_ID, "text": horoscope})


if __name__ == '__main__':
    send_message()
