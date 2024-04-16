from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.bot_logic.loader import dp
from gpt_bot import settings
from utils.statesform import StepsForm
import openai


@dp.callback_query(F.data == "AI")
async def chat_start(call: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Закончить чат", callback_data="AI")
    )
    builder.add(types.InlineKeyboardButton(
        text="Стереть память", callback_data="AI")
    )

    await call.message.answer("Отправить сообщение, чтобы начать переписку", reply_markup=builder.as_markup())
    await state.set_state(StepsForm.AI)
    await state.update_data(history=[{"question": None, "answer": None}])


@dp.message(StepsForm.AI)
async def chat_talk(message: types.Message, state: FSMContext):
    openai.api_key = settings.ACCESS_TOKEN
    data = await state.get_data()
    data = data.get('history')
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Закончить чат", callback_data="back")
    )
    builder.add(types.InlineKeyboardButton(
        text="Стереть память", callback_data="clear")
    )
    await message.answer("ИИ думает...", reply_markup=builder.as_markup())

    history = []
    if len(data) > 1:
        for index in range(0, len(data)):
            if data[index].get('question') is None:
                data[index]['question'] = message.text
                d = {"role": "user", "content": data[index]['question']}
                history.append(d)
            else:
                d = [{"role": "user", "content": data[index]['question']},
                     {"role": "assistant", "content": data[index].get('answer')}]
                history += d
    else:
        data[0]['question'] = message.text
        d = {"role": "user", "content": data[0].get('question')}
        history.append(d)
    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history,
        max_tokens=500,
        temperature=1,
    )
    resp_ai = request['choices'][0]['message']['content']
    data[-1]['answer'] = resp_ai.replace('\n', '')
    text = f"{message.from_user.username}\nQ:{data[-1]['question']}\nA:{data[-1]['answer']}"
    data.append({"question": None, "answer": None})
    if len(data) > 10:
        await state.update_data(history=[{"question": None, "answer": None}])
    await state.update_data(history=data)
    await message.answer(resp_ai)


@dp.callback_query(F.data == "clear")
async def clear(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Память ИИ стерта')
    await state.update_data(history=[{"question": None, "answer": None}])
