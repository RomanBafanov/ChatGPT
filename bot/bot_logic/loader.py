from django.conf import settings
from aiogram import Bot, Dispatcher

bot_token = settings.TELEGRAM_BOT_API_TOKEN

default_commands = (
    ('start', "Запустить бота"),
)

bot = Bot(bot_token, parse_mode="HTML")
dp = Dispatcher()
