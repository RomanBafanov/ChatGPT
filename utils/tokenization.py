from openai import OpenAI

from gpt_bot import settings


# Функция отправки chatGPT строки для ее токенизации (вычисления эмбедингов)
def get_embedding(text, model="text-embedding-ada-002"):
    api_key = settings.ACCESS_TOKEN
    client = OpenAI(api_key=api_key, base_url="https://api.proxyapi.ru/openai/v1")

    return client.embeddings.create(input=[text], model=model).data[0].embedding
