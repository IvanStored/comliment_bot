import json
from os import getenv

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()


class Settings:
    TOKEN = getenv('TOKEN')
    ADMIN_USER_ID = int(getenv('ADMIN_USER_ID'))
    RECEIVER_USER_ID = int(getenv('RECEIVER_USER_ID'))
    WEB_SERVER_HOST = '::'
    WEB_SERVER_PORT = int(getenv('WEB_SERVER_PORT'))
    WEBHOOK_PATH = '/webhook'
    BASE_WEBHOOK_URL = getenv('WEB_SERVER_HOST')
    DEEPL_API = getenv('DEEPL_API')
    HOROSCOPE_URL= 'https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily'
    CAT_TOKEN = getenv('TOKEN')
    API_URL = 'https://api.thecatapi.com/v1/images/search'
    API_PARAMS = {'x-api-key': CAT_TOKEN}
    TG_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    WORDS_DATA = json.load(open('misc.json', 'r', encoding='utf-8'))


class MetroLines:
    RED = [
        {'name': '🔴Академмістечко🔴', 'lan': 50.464861, 'lon': 30.355083},
        {'name': '🔴Житомирська🔴', 'lan': 50.4561750, 'lon': 30.3656278},
        {'name': '🔴Святошин🔴', 'lan': 50.457903, 'lon': 30.390614},
        {'name': '🔴Нивки🔴', 'lan': 50.458653, 'lon': 30.404042},
        {'name': '🔴Берестейська🔴', 'lan': 50.458333, 'lon': 30.420833},
        {'name': '🔴Шулявська🔴', 'lan': 50.455, 'lon': 30.445278},
        {'name': '🔴Політехнічний інститут🔴', 'lan': 50.450833, 'lon': 30.466111},
        {'name': '🔴Вокзальна🔴', 'lan': 50.441667, 'lon': 30.4875},
        {'name': '🔴Університет🔴', 'lan': 50.44417, 'lon': 30.50583},
        {'name': '🔴Театральна🔴', 'lan': 50.44472, 'lon': 30.51806},
        {'name': '🔴Хрещатик🔴', 'lan': 50.447260000028, 'lon': 30.52483000002778},
        {
            'name': '🔴Арсенальна🔴',
            'lan': 50.44389,
            'lon': 30.54556,
        },
        {'name': '🔴Дніпро🔴', 'lan': 50.44111, 'lon': 30.55861},
        {'name': '🔴Гідропарк🔴', 'lan': 50.44556, 'lon': 30.57694},
        {'name': '🔴Лівобережна🔴', 'lan': 50.45139, 'lon': 30.59889},
        {'name': '🔴Дарниця🔴', 'lan': 50.45556, 'lon': 30.61306},
        {'name': '🔴Чернігівська🔴', 'lan': 50.45972, 'lon': 30.63083},
        {'name': '🔴Лісова🔴', 'lan': 50.464639, 'lon': 30.64556},
    ]
    GREEN = [
        {'name': '🟢Сирець🟢', 'lan': 50.47611, 'lon': 30.43056},
        {'name': '🟢Дорогожичі🟢', 'lan': 50.47361, 'lon': 30.44944},
        {'name': '🟢Лук\'янівська🟢', 'lan': 50.46222, 'lon': 30.48167},
        {'name': '🟢Золоті ворота🟢', 'lan': 50.44833, 'lon': 30.51333},
        {'name': '🟢Палац спорту🟢', 'lan': 50.43806, 'lon': 30.52083},
        {'name': '🟢Кловська🟢', 'lan': 50.43694, 'lon': 30.53167},
        {'name': '🟢Печерська🟢', 'lan': 50.4275, 'lon': 30.53889},
        {'name': '🟢Звіринецька🟢', 'lan': 50.41806, 'lon': 30.545},
        {'name': '🟢Видубичі🟢', 'lan': 50.40222, 'lon': 30.56083},
        {'name': '🟢Славутич🟢', 'lan': 50.39417, 'lon': 30.60417},
        {'name': '🟢Осокорки🟢', 'lan': 50.39528, 'lon': 30.61611},
        {'name': '🟢Позняки🟢', 'lan': 50.39806, 'lon': 30.63333},
        {'name': '🟢Харківська🟢', 'lan': 50.40083, 'lon': 30.65222},
        {'name': '🟢Вирлиця🟢', 'lan': 50.40333, 'lon': 30.66611},
        {'name': '🟢Бориспільська🟢', 'lan': 50.40333, 'lon': 30.68278},
        {'name': '🟢Червоний хутір🟢', 'lan': 50.40889, 'lon': 30.69444},
    ]
    BLUE = [
        {'name': '🔵Героїв Дніпра🔵', 'lan': 50.5225, 'lon': 30.49861},
        {'name': '🔵Мінська🔵', 'lan': 50.51222, 'lon': 30.49833},
        {'name': '🔵Оболонь🔵', 'lan': 50.50111, 'lon': 30.49806},
        {'name': '🔵Почайна🔵', 'lan': 50.48667, 'lon': 30.49778},
        {'name': '🔵Тараса Шевченка🔵', 'lan': 50.47306, 'lon': 30.505},
        {'name': '🔵Контрактова площа🔵', 'lan': 50.465, 'lon': 30.51667},
        {'name': '🔵Поштова площа🔵', 'lan': 50.45917, 'lon': 30.52556},
        {'name': '🔵Майдан Незалежності🔵', 'lan': 50.45, 'lon': 30.52417},
        {'name': '🔵Площа Українських Героїв🔵', 'lan': 50.43944, 'lon': 30.51694},
        {'name': '🔵Олімпійська🔵', 'lan': 50.43194, 'lon': 30.51639},
        {'name': '🔵Палац «Україна»🔵', 'lan': 50.42083, 'lon': 30.52083},
        {'name': '🔵Либідська🔵', 'lan': 50.420833, 'lon': 30.520833},
        {'name': '🔵Деміївська🔵', 'lan': 50.4047917, 'lon': 30.5168333},
        {'name': '🔵Голосіївська🔵', 'lan': 50.3975, 'lon': 30.50833},
        {'name': '🔵Васильківська🔵', 'lan': 50.39333, 'lon': 30.48806},
        {'name': '🔵Виставковий центр🔵', 'lan': 50.3825806, 'lon': 30.4775361},
        {'name': '🔵Іподром🔵', 'lan': 50.3765556, 'lon': 30.4691167},
        {'name': '🔵Теремки🔵', 'lan': 50.3670444, 'lon': 30.4542028},
    ]
    ALL = RED + GREEN + BLUE

BOT = Bot(Settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
