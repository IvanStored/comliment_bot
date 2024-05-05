import logging
import sys
from os import getenv

from aiohttp import web

from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from aiogram.utils.markdown import hbold
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from dotenv import load_dotenv

from process_compliments import get_random_compliment

load_dotenv()
TOKEN = getenv("TOKEN")

WEB_SERVER_HOST = "::"
WEB_SERVER_PORT = int(getenv("WEB_SERVER_PORT"))

WEBHOOK_PATH = "/webhook"
BASE_WEBHOOK_URL = getenv("WEB_SERVER_HOST")

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@router.message(Command("compliment"))
async def sent_compliment(message: Message) -> None:
    compliment = get_random_compliment()
    await message.answer(text=compliment)


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}")


def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    dp.startup.register(on_startup)

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    app = web.Application()
    bot.set_my_commands(
        commands=[
            BotCommand(
                command="compliment",
                description="Випадковий комплімент"
            ),
        ]
    )
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
