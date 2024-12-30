from django.db import models


class KnowledgeBase(models.Model):
    question = models.CharField(verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    embedding = models.JSONField(verbose_name="Эмбединг", default=None, null=True, blank=True)

    def __str__(self):
        return str(self.question)

    class Meta:
        verbose_name = 'знание'
        verbose_name_plural = 'База знаний'
