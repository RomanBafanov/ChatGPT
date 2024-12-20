# ChatGPT
 
Чат с ИИ

## Как установить

Создайте виртуальное окружение

```bash
python -m venv venv
``` 

Активируйте виртуальное окружение

```bash
source venv/bin/activate
``` 

Python3 должен быть уже установлен. Затем используйте pip 
(или pip3, если есть конфликт с Python2) для установки зависимостей:

```bash
pip install -r requirements.txt
``` 

### будут установлены:

_
- Django~=5.0.4
- python-dotenv~=1.0.1
- aiogram~=3.4.1
- openai~=1.35

## Заполнение файла паролей

Создайте файл .env и заполните его следующими данными:

BOT_TOKEN='Токен вашего бота полученного от BotFather'
ACCESS_TOKEN='Токен от OpenAI полученный по средством регистрации на сайте proxyapi.ru'

## Использование

Команда 
```bash
python manage.py bot
```

Запускает бота
