from django.core.management import BaseCommand
from bot.bot_logic.loader import bot, dp
from bot.bot_logic import handlers
import asyncio


async def main():
    await dp.start_polling(bot)


class Command(BaseCommand):
    help = 'Команда для запуска Telegram-бота.'

    def handle(self, *args, **kwargs):
        asyncio.run(main())
