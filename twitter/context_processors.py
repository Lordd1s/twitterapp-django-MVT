from django.http import HttpRequest

from twitter import models


def get_post_count(request: HttpRequest) -> dict[str, any]:
    """Возвращает количество одобренных книг на веб-платформе."""

    return {"post_count": models.Post.objects.filter(is_moderate=True).count()}
