from django.http import HttpRequest

from twitter import models


def get_post_count(request: HttpRequest) -> dict[str, any]:
    """Возвращает количество одобренных постов на веб-платформе."""

    return {"post_count": models.Post.objects.filter(is_moderate=True).count()}


def get_status_of_message(request: HttpRequest) -> dict[str, any]:
    if request.user.is_authenticated:
        return {
            "message_status_count": models.Message.objects.filter(
                recipient=request.user, is_viewed=False
            ).count()
        }
    else:
        return {"message_status_count": "Non authorized!"}
