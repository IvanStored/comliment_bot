import datetime
import logging
import os
import random
import sys
from os import getenv

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiohttp import web
from aiogram.enums import ParseMode, ContentType
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)
from dotenv import load_dotenv

from google_photos import get_random_image_url
from process_files import get_random_compliment, get_random_motivation
from hangman import get_random_word
from random_cat_image import get_random_cat_image_url

load_dotenv()
TOKEN = getenv("TOKEN")
ADMIN_USER_ID = int(getenv("ADMIN_USER_ID"))
RECEIVER_USER_ID = int(getenv("RECEIVER_USER_ID"))
WEB_SERVER_HOST = "::"
WEB_SERVER_PORT = int(getenv("WEB_SERVER_PORT"))

WEBHOOK_PATH = "/webhook"
BASE_WEBHOOK_URL = getenv("WEB_SERVER_HOST")
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
router = Router()
ANSWERS = [
    "Це однозначно так.",
    "Без сумніву.",
    "Так, однозначно.",
    "Можеш покластися на це.",
    "Як я бачу, то так.",
    "Ймовірно.",
    "Перспективи хороші.",
    "Так.",
    "Знаки вказують на те, що так.",
    "Відповідь нечітка, спробуйте ще раз.",
    "Спитай пізніше.",
    "Краще зараз тобі не відповідати.",
    "Не можу передбачити зараз.",
    "Сконцентруйся та спитай ще раз.",
    "Не розраховуй на це.",
    "Моя відповідь - ні.",
    "Мої джерела кажуть ні.",
    "Перспективи не дуже хороші.",
    "Дуже сумнівно.",
    "Звичайно ні.",
    "Бог каже так.",
    "Бог каже ні.",
    "Ніхто не знає.",
    "Я так не думаю.",
]
games = {}


class HangmanState(StatesGroup):
    waiting_for_letter = State()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Привіт, сонечко. Просто тисни на меню та обери потрібну тобі зараз команду"
    )


@router.message(Command("mirror"))
async def send_cat_image(message: Message) -> None:
    image_url = get_random_cat_image_url()
    await message.answer_photo(photo=image_url)


@router.message(Command("random_photo"))
async def send_random_image(message: Message) -> None:
    image_url = get_random_image_url()
    await message.answer_photo(photo=image_url)


@router.message(Command("compliment"))
async def send_compliment(message: Message) -> None:
    compliment = get_random_compliment()
    await message.answer(text=compliment)


@router.message(Command("motivation"))
async def send_motivation(message: Message) -> None:
    motivation = get_random_motivation()
    await message.answer(text=motivation)


@router.message(Command("days"))
async def calculate_days(message: Message) -> None:
    today = datetime.date.today()
    start_date = datetime.date(year=2020, month=8, day=2)
    total_days = today - start_date
    days_str = "днів"
    if str(total_days.days).endswith("1"):
        days_str = "день"
    elif str(total_days.days).endswith("2"):
        days_str = "дня"
    message_text = (
        f"Ми провели {total_days.days} {days_str} разом, дякую тобі!!!"
    )
    await message.answer(text=message_text)


@router.message(Command("magic_ball"))
async def get_answer(message: Message) -> None:
    await message.answer(text=random.choice(ANSWERS))


@router.message(Command("new_game"))
async def new_game(message: Message, state: FSMContext):
    word = get_random_word()
    games[message.from_user.id] = {
        "word": word.strip().replace("\n", ""),
        "guessed": ["_" for _ in range(len(word)-1)],
        "tries": 7,
        "wrong_guesses": [],
    }
    await message.reply(
        f"Нова гра почата! Слово: {' '.join(games[message.from_user.id]['guessed'])}"
    )
    await state.set_state(HangmanState.waiting_for_letter)


@router.message(HangmanState.waiting_for_letter)
async def guess_letter(message: Message, state: FSMContext):
    game = games.get(message.from_user.id)
    letter = message.text.lower()
    if not letter.isalpha() or len(letter) != 1:
        await message.reply("Це не буква")
        return
    if letter in game["guessed"] or letter in game["wrong_guesses"]:
        await message.reply("Ти вже вгадала цю букву, спробуй іншу.")
        return

    if letter in game["word"]:
        for index, char in enumerate(game["word"]):
            if char == letter:
                game["guessed"][index] = letter
        await message.reply(f"Молодець! Слово: {' '.join(game['guessed'])}")
    else:
        game["tries"] -= 1
        game["wrong_guesses"].append(letter)
        await message.reply(
            f"Неправильно( В тебе лишилося {game['tries']} спроб.\nНеправильні букви: {', '.join(game['wrong_guesses'])}"
        )

    if "_" not in game["guessed"]:
        await message.reply(f"Молодець! Ти вгадала слово: {game['word']}")
        await state.clear()
        games.pop(message.from_user.id, None)
    elif game["tries"] == 0:
        await message.reply(f"Гра завершена! Слово було: {game['word']}")
        await state.clear()
        games.pop(message.from_user.id, None)


@router.message()
async def echo_handler(message: Message) -> None:
    if message.from_user.id == ADMIN_USER_ID:
        try:
            await message.send_copy(chat_id=RECEIVER_USER_ID)
            await message.answer(text="message sended")
        except TypeError:
            await message.answer("Nice try!")


async def on_startup(bot: Bot) -> None:
    await bot.set_my_commands(
        commands=[
            BotCommand(
                command="compliment", description="Випадковий комплімент"
            ),
            BotCommand(
                command="motivation",
                description="Тисни сюди, коли треба трохи мотивації",
            ),
            BotCommand(
                command="days", description="Скільки чудових днів ми разом"
            ),
            BotCommand(
                command="mirror",
                description="Це дзеркало, просто натисни і побачиш себе",
            ),
            BotCommand(
                command="magic_ball",
                description="Якщо не впевнена в рішенні, подумки задай питання та натисни сюди",
            ),
            BotCommand(
                command="new_game", description="Гра в шибеницю, якщо нудно)"
            ),
            BotCommand(
                command="random_photo", description="Випадкова наша фотка (чи тільки твоя, там трохи є)"
            ),
        ]
    )
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}")


def main(bot) -> None:
    dp = Dispatcher()
    dp.include_router(router)

    dp.startup.register(on_startup)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main(bot=bot)
