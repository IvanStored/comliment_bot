import logging
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from core.commands import BOT_COMMANDS
from core.routers import router
from settings import Settings, BOT


async def on_startup(bot: Bot) -> None:
    await bot.set_my_commands(commands=BOT_COMMANDS)
    await bot.set_webhook(f'{Settings.BASE_WEBHOOK_URL}{Settings.WEBHOOK_PATH}')


def main(bot: Bot) -> None:
    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(on_startup)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path=Settings.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=Settings.WEB_SERVER_HOST, port=Settings.WEB_SERVER_PORT)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main(BOT)
