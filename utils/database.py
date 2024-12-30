from bot.models import KnowledgeBase
from utils.tokenization import get_embedding


def save_embedding():
    base = KnowledgeBase.objects.all()
    for question in base:
        if not question.embedding:
            text = f"{question.question} {question.answer}"
            embedding = get_embedding(text)
            question.embedding = embedding
            question.save()


def get_data():
    data = []
    base = KnowledgeBase.objects.all()
    for question in base:
        text = f"{question.question} {question.answer}"
        data.append((text, question.embedding))

    return data
