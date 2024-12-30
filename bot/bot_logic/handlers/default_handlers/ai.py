from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asgiref.sync import sync_to_async
from scipy import spatial
import tiktoken
from openai import OpenAI

from bot.bot_logic.loader import dp
from gpt_bot import settings
from utils.database import save_embedding, get_data
from utils.statesform import StepsForm
from utils.tokenization import get_embedding

system = {"role": "system", "content": ""}
GPT_MODEL = "gpt-3.5-turbo"


def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Возвращает число токенов в строке для заданной модели"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


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
    await sync_to_async(save_embedding)()

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
    # print(data_conversation)

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Закончить чат", callback_data="back")
    )
    builder.add(types.InlineKeyboardButton(
        text="Стереть память", callback_data="clear")
    )
    await message.answer("ИИ думает...", reply_markup=builder.as_markup())

    user_text = get_embedding(message.text)

    data_from_the_database = await sync_to_async(get_data)()
    relatedness_fn = lambda x, y: 1 - spatial.distance.cosine(x, y)
    strings_and_relatednesses = [
        (data[0], relatedness_fn(user_text, data[1]))
        for data in data_from_the_database
    ]
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    token_budget = 4096 - 500
    start_message = ("Используй приведённые ниже вопросы и ответы, чтобы ответить на следующий вопрос. "
                     "Если ответ не найден напиши 'Я не смог найти ответ'\n")
    for string in strings:
        next_article = f'\n\nWikipedia article section:\n"""\n{string}\n"""'
        if (num_tokens(start_message + next_article + message.text, model=GPT_MODEL) > token_budget):
            break
        else:
            start_message += next_article
    final_message = start_message + message.text

    if len(data_conversation) > 1:
        # answer = data.get('answer')
        answer = get_embedding(data.get('answer'))
        data_conversation.append({"role": "assistant", "content": answer})
        data_conversation.append({"role": "user", "content": final_message})
    else:
        data_conversation.append({"role": "user", "content": final_message})

    completion = client.chat.completions.create(
        model=GPT_MODEL,
        messages=data_conversation
    )
    # print(data_conversation)
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
