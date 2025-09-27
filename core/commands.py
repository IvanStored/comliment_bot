from aiogram.types import BotCommand

BOT_COMMANDS = [
    BotCommand(command='compliment', description='Випадковий комплімент'),
    BotCommand(command='motivation', description='Тисни сюди, коли треба трохи мотивації'),
    BotCommand(command='days', description='Скільки чудових днів ми разом'),
    BotCommand(command='mirror', description='Це дзеркало, просто натисни і побачиш себе'),
    BotCommand(
        command='magic_ball', description='Якщо не впевнена в рішенні, подумки задай питання та натисни сюди'
    ),
    BotCommand(command='new_game', description='Гра в шибеницю, якщо нудно)'),
    BotCommand(command='horoscope', description='Гороскоп на сьогоднішній день'),
    BotCommand(command='random_station', description='Рандомна станція метро'),
    BotCommand(command='nearest_station', description='Найближча станція метро')
]
