from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator


# Create your models here.


class UserProfile(models.Model):
    """User profile"""

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to="images/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "png", "gif", "jpeg"]),
        ],
        default="6596121.png",
    )
    was_born = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    first_name = models.CharField(max_length=50, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=50, blank=True, verbose_name="Фамилия")

    class Meta:
        app_label = "twitter"
        ordering = ("-was_born", "user")
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Профиль {self.user}"


class Message(models.Model):
    sender = models.ForeignKey(
        to=User,
        related_name="sent_messages",
        on_delete=models.CASCADE,
        verbose_name="Отправитель",
    )
    recipient = models.ForeignKey(
        to=User,
        related_name="received_messages",
        on_delete=models.CASCADE,
        verbose_name="Получатель",
    )
    subject = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Тема сообщений"
    )
    text = models.TextField(verbose_name="Текст сообщений", blank=False)
    timestamp = models.DateTimeField(default=timezone.now)
    answered = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    is_opened = models.BooleanField(default=False)
    is_viewed = models.BooleanField(default=False)

    class Meta:
        app_label = "twitter"
        ordering = ["-timestamp", "subject"]
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"Сообщение {self.sender} -> {self.recipient}"


class Post(models.Model):
    """Post model"""

    author = models.ForeignKey(
        to=User, max_length=50, on_delete=models.CASCADE, verbose_name="Автор"
    )
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(max_length=1000, verbose_name="Описание")
    image = models.ImageField(
        upload_to="images/posts",
        verbose_name="Изображение",
        default=None,
        null=True,
        blank=True,
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
        verbose_name="Дата комментирования", default=timezone.now
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
