import requests
from settings import Settings
from utils.utils import translate_horoscope_data, get_horoscope_for_today


def send_message() -> None:
    horoscope = translate_horoscope_data(english_data=get_horoscope_for_today(), api_key=Settings.DEEPL_API)
    requests.post(url=Settings.TG_URL, data={"chat_id": Settings.RECEIVER_USER_ID, "text": horoscope})


if __name__ == '__main__':
    send_message()
