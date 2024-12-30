from django.contrib import admin

from bot.models import KnowledgeBase


@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'embedding')  # Что будет отображено
    list_display_links = ('question',)  # Кликая на данное поле вы можете перейти к сущьности данного поля
    # search_fields = ('id', 'tg_id', 'name', 'full_name', 'phone')  # По каким полям осуществляется поиск
    # list_filter = ('age',)  # По каким полям осуществляется фильтрация
