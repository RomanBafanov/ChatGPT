from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.bot_logic.loader import dp
from gpt_bot import settings
from utils.statesform import StepsForm
from openai import OpenAI


system = {"role": "system", "content": ""}


@dp.callback_query(F.data == "AI")
async def chat_start(call: types.CallbackQuery, state: FSMContext):
    """
    Функция запускает чат с ИИ

    :param call: (CallbackQuery) информация о нажатой кнопке "Начать чат с ИИ".
    :param state: (FSMContext) информация о состоянии пользователя.
    :return: Выводин на экран сообщение о начале общения с ИИ
    """

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Закончить чат", callback_data="back")
    )
    builder.add(types.InlineKeyboardButton(
        text="Стереть память", callback_data="clear")
    )

    await call.message.answer("Отправить сообщение, чтобы начать переписку", reply_markup=builder.as_markup())
    await state.set_state(StepsForm.AI)
    await state.update_data(history=[system])


@dp.message(StepsForm.AI)
async def chat_talk(message: types.Message, state: FSMContext):
    """
    Функция осуществляет связь с чатом ГПТ и выдаёт ответ от ИИ

    :param message: (Message) информация о сообщении пользователя.
    :param state: (FSMContext) информация о состоянии пользователя.
    :return: Возвращает пользователю ответ от ИИ
    """

    # openai.api_key = settings.ACCESS_TOKEN
    api_key = settings.ACCESS_TOKEN
    data = await state.get_data()
    data_conversation = data.get('history')
    client = OpenAI(api_key=api_key, base_url="https://api.proxyapi.ru/openai/v1")
    print(data_conversation)

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Закончить чат", callback_data="back")
    )
    builder.add(types.InlineKeyboardButton(
        text="Стереть память", callback_data="clear")
    )
    await message.answer("ИИ думает...", reply_markup=builder.as_markup())

    if len(data_conversation) > 1:
        answer = data.get('answer')
        data_conversation.append({"role": "assistant", "content": answer})
        data_conversation.append({"role": "user", "content": message.text})
    else:
        data_conversation.append({"role": "user", "content": message.text})

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=data_conversation
    )
    print(data_conversation)
    answer = completion.choices[0].message.content
    await state.update_data(history=data_conversation)
    await state.update_data(answer=answer)
    await message.answer(f"{answer}")


@dp.callback_query(F.data == "clear")
async def clear(call: types.CallbackQuery, state: FSMContext):
    """
    Функция осуществляет очистку памяти общения с ИИ

    :param call: (CallbackQuery) информация о нажатой кнопке "Стереть память".
    :param state: (FSMContext) информация о состоянии пользователя.
    :return: Возвращает сообщение, что память общения с ИИ стёрта
    """

    await call.message.answer('Память ИИ стерта')
    await state.update_data(history=[system])
