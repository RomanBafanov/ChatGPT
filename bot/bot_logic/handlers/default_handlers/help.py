from aiogram import types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.bot_logic.loader import dp


@dp.message(Command("help"))
async def bot_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Начать чат с ИИ", callback_data="AI")
    )
    await message.answer("Это тестовый бот. Тут ты можешь пообщаться с ИИ и только...",
                         reply_markup=builder.as_markup())