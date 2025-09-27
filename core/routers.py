import datetime
import random

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from settings import Settings, MetroLines, BOT
from utils.metro_helpers import find_closest_lat_lon
from utils.utils import get_horoscope_for_today, translate_horoscope_data, get_random_cat_image_url

router = Router()
GAMES = {}


class HangmanState(StatesGroup):
    waiting_for_letter = State()


@router.message(Command('horoscope'))
async def send_horoscope(message: Message) -> None:
    horoscope_data = get_horoscope_for_today()
    translated_horoscope = translate_horoscope_data(english_data=horoscope_data, api_key=Settings.DEEPL_API)
    text = f'Твій гороскоп на сьогоднішній день:\n{translated_horoscope}'
    await message.answer(text=text)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer('Привіт, сонечко. Просто тисни на меню та обери потрібну тобі зараз команду')


@router.message(Command('mirror'))
async def send_cat_image(message: Message) -> None:
    image_url = get_random_cat_image_url()
    await message.answer_photo(photo=image_url)


@router.message(Command('compliment'))
async def send_compliment(message: Message) -> None:
    await message.answer(text=random.choice(Settings.WORDS_DATA['compliments']))


@router.message(Command('motivation'))
async def send_motivation(message: Message) -> None:
    await message.answer(text=random.choice(Settings.WORDS_DATA['motivation']))


@router.message(Command('days'))
async def calculate_days(message: Message) -> None:
    today = datetime.date.today()
    start_date = datetime.date(year=2020, month=8, day=2)
    total_days = today - start_date
    days_str = 'днів'
    if str(total_days.days).endswith('1'):
        days_str = 'день'
    elif str(total_days.days).endswith('2'):
        days_str = 'дня'
    message_text = (
        f'Ми провели {total_days.days} {days_str} разом, дякую тобі!!!'
    )
    await message.answer(text=message_text)


@router.message(Command('magic_ball'))
async def get_answer(message: Message) -> None:
    await message.answer(text=random.choice(Settings.WORDS_DATA['magic_ball']))


@router.message(Command('new_game'))
async def new_game(message: Message, state: FSMContext):
    word = random.choice(Settings.WORDS_DATA['words'])
    GAMES[message.from_user.id] = {
        'word': word.strip().replace('\n', ''),
        'guessed': ['_' for _ in range(len(word)-1)],
        'tries': 7,
        'wrong_guesses': [],
    }
    await message.reply(
        f'Нова гра почата! Слово: {' '.join(GAMES[message.from_user.id]['guessed'])}'
    )
    await state.set_state(HangmanState.waiting_for_letter)


@router.message(HangmanState.waiting_for_letter)
async def guess_letter(message: Message, state: FSMContext):
    game = GAMES.get(message.from_user.id)
    letter = message.text.lower()
    if not letter.isalpha() or len(letter) != 1:
        await message.reply('Це не буква')
        return
    if letter in game['guessed'] or letter in game['wrong_guesses']:
        await message.reply('Ти вже вгадала цю букву, спробуй іншу.')
        return

    if letter in game['word']:
        for index, char in enumerate(game['word']):
            if char == letter:
                game['guessed'][index] = letter
        await message.reply(f'Молодець! Слово: {' '.join(game['guessed'])}')
    else:
        game['tries'] -= 1
        game['wrong_guesses'].append(letter)
        await message.reply(
            f'Неправильно( В тебе лишилося {game['tries']} спроб.\nНеправильні букви: {', '.join(game['wrong_guesses'])}'
        )

    if '_' not in game['guessed']:
        await message.reply(f'Молодець! Ти вгадала слово: {game['word']}')
        await state.clear()
        GAMES.pop(message.from_user.id, None)
    elif game['tries'] == 0:
        await message.reply(f'Гра завершена! Слово було: {game['word']}')
        await state.clear()
        GAMES.pop(message.from_user.id, None)

@router.message(Command('random_station'))
async def full_random_station(message: Message) -> None:
    random_station = random.choice(MetroLines.ALL)
    await BOT.send_location(
        chat_id=message.chat.id,
        latitude=random_station['lan'],
        longitude=random_station['lon'],
    )
    await message.answer(text=random_station['name'])


@router.message(Command('nearest_station'))
async def handle_user_location(message: Message) -> None:
    await message.answer(
        text='Для пошуку найближчої станції надішліть своє місцезнаходження'
    )


@router.message(lambda message: message.content_type in ['location', 'venue'])
async def nearest_metro_station(message: Message) -> None:
    lan = message.location.latitude
    lon = message.location.longitude
    station = find_closest_lat_lon(data=MetroLines.ALL, v={'lan': lan, 'lon': lon})
    await message.answer(text=f'Найближча до вас станція - {station['name']}')
    await BOT.send_location(
        chat_id=message.chat.id,
        latitude=station['lan'],
        longitude=station['lon']
    )
