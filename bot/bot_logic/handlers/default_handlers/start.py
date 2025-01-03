from aiogram import types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.bot_logic.loader import dp, bot
from utils.set_bot_command import set_bot_commands


@dp.message(Command("start"))
async def bot_start(message: types.Message):
    """
    Функция обработчик стартовой команды бота, проводит проверку на регистрацию

    :param message: (Message) информация о сообщении пользователя.
    :return: Выводит сообщение с приветствием пользователю и кнопку для начала общения с ИИ
    """

    await set_bot_commands(bot)
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Начать чат с ИИ", callback_data="AI")
    )
    await message.answer(f"Привет, {message.from_user.full_name}! "
                         f"Хочешь поболтать с искусственным интеллектом?", reply_markup=builder.as_markup())


@dp.callback_query(F.data == "back")
async def back(callback: types.CallbackQuery, state: FSMContext):
    """
    Функция дублирует стартовую функцию

    :param callback: (CallbackQuery) информация о нажатой кнопке "Закончить чат".
    :param state: (FSMContext) информация о состоянии пользователя.
    :return: Выводит сообщение с приветствием пользователю и кнопку для начала общения с ИИ
    """

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Начать чат с ИИ", callback_data="AI")
    )
    await callback.message.answer(f"Привет, {callback.from_user.full_name}! "
                                  f"Может ещё поболтаем?", reply_markup=builder.as_markup())
    await state.clear()
