import datetime
import logging
import sys
from os import getenv

from aiohttp import web

from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)
from dotenv import load_dotenv

from process_files import get_random_compliment, get_random_motivation
from random_cat_image import get_random_cat_image_url

load_dotenv()
TOKEN = getenv("TOKEN")

WEB_SERVER_HOST = "::"
WEB_SERVER_PORT = int(getenv("WEB_SERVER_PORT"))

WEBHOOK_PATH = "/webhook"
BASE_WEBHOOK_URL = getenv("WEB_SERVER_HOST")

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Привіт, сонечко. Просто тисни на меню та обери потрібну тобі зараз команду"
    )


@router.message(Command("mirror"))
async def send_cat_image(message: Message) -> None:
    image_url = get_random_cat_image_url()
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
        ]
    )
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}")


def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    dp.startup.register(on_startup)

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

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
    main()
