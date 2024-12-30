import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from dotenv.main import load_dotenv

load_dotenv()


def add_admin(username, password):
    user = get_user_model().objects.filter(username=username).first()
    if not user:
        get_user_model().objects.create_superuser(username=username, password=password, email='')


class Command(BaseCommand):
    help = 'Команда для создания администратора, если он ещё не создан'

    def handle(self, *args, **kwargs):
        username = os.environ.get('ADMIN_USER')
        password = os.environ.get('ADMIN_PASSWORD')
        add_admin(username, password)