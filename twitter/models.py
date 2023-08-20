from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    """Post model"""

    author = models.ForeignKey(
        to=User, max_length=50, on_delete=models.CASCADE, verbose_name="Автор"
    )
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(max_length=1000, verbose_name="Описание")
    image = models.ImageField(
        upload_to="images/posts", verbose_name="Изображение", default=None
    )
    date_created = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    is_moderate = models.BooleanField(default=False, verbose_name="Прошел ли модерацию")

    class Meta:
        """Используемые метаданные"""

        app_label = "twitter"
        ordering = ("-date_created",)
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        """Показывание метаданные"""
        if self.is_moderate:
            status = "Прошел модерацию"
        else:
            status = "На проверке"
        return f"{self.author} - {self.title} - {status}"


class Comment(models.Model):
    author = models.ForeignKey(
        to=User, verbose_name="Автор коммента", on_delete=models.CASCADE
    )
    post = models.ForeignKey(to=Post, verbose_name="ID Поста", on_delete=models.CASCADE)
    comment = models.TextField(verbose_name="Комментарии", max_length=200)
    comment_data = models.DateTimeField(
        verbose_name="Дата комментирования", default=timezone.now()
    )

    class Meta:
        app_label = "twitter"
        ordering = ("-comment_data", "post_id")
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментария"

    def __str__(self):
        return f"{self.author} - оставил коментарий по этой дате -> {self.comment_data}"

    def get_current_comment_rating(self):
        # print(self)
        ratings = CommentRatings.objects.filter(comment=self)
        likes = ratings.filter(status=True).count()
        dislikes = ratings.filter(status=False).count()
        rating = likes - dislikes

        return rating

    def get_comments_ratings_count(self):
        ratings = CommentRatings.objects.filter(comment=self).count()
        return ratings


class CommentRatings(models.Model):
    author = models.ForeignKey(
        to=User, verbose_name="Автор лайка", on_delete=models.CASCADE
    )
    comment = models.ForeignKey(
        to=Comment, verbose_name="ID Коммента", on_delete=models.CASCADE
    )
    status = models.BooleanField(default=False)

    class Meta:
        app_label = "twitter"
        ordering = ("-comment_id", "author")
        verbose_name = "Рейтинг к коментарию"
        verbose_name_plural = "Рейтинги к коментариям"

    def __str__(self):
        if self.status:
            like = "ЛАЙК"
        else:
            like = "ДИЗЛАЙК"
        return f"{self.author} {like}"


class Ratings(models.Model):
    """Рейтинг к новости"""

    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        app_label = "twitter"
        ordering = ("-post", "author")
        verbose_name = "Рейтинг к посту"
        verbose_name_plural = "Рейтинги к постам"

    def __str__(self):
        if self.status:
            like = "ЛАЙК"
        else:
            like = "ДИЗЛАЙК"
        return f"{self.author} {like}"
