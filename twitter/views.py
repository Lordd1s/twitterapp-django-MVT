import datetime
import random
import re
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from twitter import models
from twitter.models import Post, Comment
from twitter import utils


logger = logging.getLogger(__name__)


def log_exceptions(view_func):
    def wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            # Логирование ошибки
            logger.exception("An error occurred: %s", str(e))
            with open("log.txt", "a") as f:
                f.write(str(e), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    return wrapped_view


# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    """Return to home page"""
    return render(request=request, template_name="home.html")


@log_exceptions
def register(request: HttpRequest) -> HttpResponse:
    """Register a new user."""
    if request.method == "GET":
        return render(request=request, template_name="login-registration.html")

    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        regex_password = (
            r"^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-_]).{8,}$"
        )
        regex_email = r"[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}"
        email = request.POST.get("email")

        if not (username and password and email):
            return render(
                request=request,
                template_name="login-registration.html",
                context={"error": "Заполните все поля."},
            )

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return render(
                request=request,
                template_name="login-registration.html",
                context={"error": "Пользователь уже существует."},
            )

        # Check if the email is already in use
        if User.objects.filter(email=email).exists():
            return render(
                request=request,
                template_name="login-registration.html",
                context={"error": "Почта уже зарегистрирована."},
            )

        # Create the new user
        if re.match(regex_password, string=password) and re.match(
            regex_email, string=email
        ):
            new_user = User.objects.create(
                username=username, password=make_password(password), email=email
            )
            models.UserProfile.objects.create(user=new_user)

            # Log in the newly registered user
            login(request, user=new_user)
            print("successfully created new user")
            return redirect(reverse("home"))
        else:
            return render(
                request=request,
                template_name="login-registration.html",
                context={
                    "error": "Почта или пароль не соответсвует требованием!",
                    "condition": "Пароль должен содержать мин. 8 символов, одна заглавная буква, одна цифра, спец. символы: #?!@$%^&*-_",
                },
            )


@login_required
@log_exceptions
def profile(request: HttpRequest) -> HttpResponse:
    profile_db = models.UserProfile.objects.get(user=request.user)
    if request.method == "GET":
        return render(
            request=request,
            template_name="profile.html",
            context={"profile": profile_db},
        )
    elif request.method == "POST":
        avatar = request.FILES.get("avatar")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        was_born = request.POST.get("was_born")
        profile_db.avatar = avatar
        profile_db.first_name = first_name
        profile_db.last_name = last_name
        profile_db.was_born = was_born
        profile_db.save()
        return redirect(reverse("profile"))


@login_required
@log_exceptions
def delete_profile(request: HttpRequest) -> HttpResponse:
    user = models.User.objects.get(username=request.user)
    logout(request)
    user.delete()
    return redirect(reverse("home"))


@log_exceptions
def login_user(request: HttpRequest) -> HttpResponse:
    """Login a user."""
    if request.method == "GET":
        return render(request=request, template_name="login-registration.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print(request.body)
        if not (username and password):
            # print(username, password)
            return render(
                request=request,
                template_name="login-registration.html",
                context={"error": "Invalid credentials."},
            )

        user = authenticate(
            username=username,
            password=password,
        )
        print(user)

        # try:
        #     login(request, user=user)
        # except Exception as e:
        #     print(e)

        if user is not None:
            # print(user)
            # User is valid, and login is successful.
            login(request, user=user)
            return redirect(reverse("home"))
        else:
            print(user)
            # Invalid login credentials.
            return render(
                request=request,
                template_name="login-registration.html",
                context={"error": "Не существует такого пользователя."},
            )


@log_exceptions
def logout_user(request: HttpRequest) -> HttpResponse:
    """Logout a user."""
    logout(request)

    return redirect(reverse("home"))


@login_required
@log_exceptions
def message(request: HttpRequest) -> HttpResponse:
    users = User.objects.all()
    context = {"users": users, "error": "Ошибка"}
    if request.method == "GET":
        return render(
            request=request, template_name="message.html", context={"users": users}
        )
    elif request.method == "POST":
        recipient = request.POST.get("recipient")
        subject = request.POST.get("subject").strip()
        messages = request.POST.get("message").strip()

        if recipient is None or subject == "" or messages == "":
            context["error"] = "Заполните все поля"
            return render(
                request=request, template_name="message.html", context=context
            )

        if users.get(username=recipient) == request.user:
            return render(
                request=request, template_name="message.html", context=context
            )

        models.Message.objects.create(
            sender=request.user,
            recipient=users.get(username=recipient),
            subject=subject,
            text=messages,
        )

        return redirect(reverse("all_messages"))


@login_required
@log_exceptions
def all_messages(request: HttpRequest) -> HttpResponse:
    mess = models.Message.objects.all()
    to_update_status = mess.filter(recipient=request.user, is_deleted=False)
    to_update_status.update(is_viewed=True)

    context = {
        "incoming_messages": to_update_status,
        "sent_messages": mess.filter(sender=request.user, is_deleted=False),
    }
    return render(
        request=request,
        template_name="all_messages.html",
        context=context,
    )


@login_required
@log_exceptions
def detail_message(
    request: HttpRequest, sender_id, recipient_id, subject=None
) -> HttpResponse:
    try:
        message_detail = models.Message.objects.get(
            sender=int(sender_id),
            recipient=int(recipient_id),
            subject=str(subject),
            is_deleted=False,
        )
    except ValueError:
        raise Http404("Неверный идентификатор пользователя")
    except ObjectDoesNotExist:
        raise Http404("Пользователь не найден")

    if request.method == "GET":
        message_detail.is_opened = True
        message_detail.save()
        return render(
            request=request,
            template_name="detail_message.html",
            context={"details": message_detail},
        )

    elif request.method == "POST":
        text = request.POST.get("text").strip()
        if text == "":
            return render(
                request=request,
                template_name="detail_message.html",
                context={
                    "details": message_detail,
                    "error": "Поле не должно быть пустым!",
                },
            )
        models.Message.objects.create(
            sender=request.user,
            recipient=message_detail.sender,
            text=text,
            subject=message_detail.subject,
            answered=True,
        )
        message_detail.replied = True
        message_detail.save()
        return redirect(reverse("all_messages"))


@login_required
@log_exceptions
def delete_message(
    request: HttpRequest,
    sender_id: str,
    recipient_id: str,
    subject=None,
) -> HttpResponse:
    if request.method == "GET":
        try:
            message_delete = models.Message.objects.get(
                sender=int(sender_id),
                recipient=int(recipient_id),
                is_deleted=False,
                subject=str(subject),
            )
            message_delete.is_deleted = True
            message_delete.save()
            return redirect(reverse("all_messages"))
        except ValueError:
            raise Http404("Неверный идентификатор пользователя")
        except ObjectDoesNotExist:
            raise Http404("Пользователь не найден")


@login_required
@log_exceptions
def edit_message(
    request: HttpRequest,
    sender_id: str,
    recipient_id: str,
    subject=None,
) -> HttpResponse:
    try:
        to_edit_message = models.Message.objects.get(
            sender=int(sender_id),
            recipient=int(recipient_id),
            is_deleted=False,
            subject=str(subject),
        )
    except (ValueError, models.Message.DoesNotExist):
        raise Http404("Сообщение не найдено")

    if request.method == "GET":
        return render(request, "edit_message.html", {"details": to_edit_message})

    elif request.method == "POST":
        subject = request.POST.get("subject").strip()
        text = request.POST.get("text").strip()

        if not subject or not text:
            return render(
                request,
                "edit_message.html",
                {"details": to_edit_message, "errors": "Заполните все поля!"},
            )

        to_edit_message.subject = subject
        to_edit_message.text = text
        to_edit_message.is_edited = True
        to_edit_message.save()
        return redirect(reverse("all_messages"))


@login_required
@log_exceptions
def all_posts(request: HttpRequest) -> HttpResponse:
    """Returns all the posts"""
    posts = models.Post.objects.all().filter(is_moderate=True).order_by("-date_created")

    if request.method == "GET":
        return render(
            request=request,
            template_name="posts.html",
            context={
                "posts": posts,
            },
        )
    elif request.method == "POST":
        # Searches for posts based on the provided search query

        search_request = request.POST.get("search")

        if search_request is None or search_request.strip() == "":
            return redirect(reverse("all_posts"))

        else:
            return render(
                request=request,
                template_name="posts.html",
                context={
                    "posts": models.Post.objects.filter(title__icontains=search_request)
                },
            )


@login_required
@log_exceptions
def add_post(request: HttpRequest) -> HttpResponse:
    """Add a post"""
    if request.method == "GET":
        return render(request=request, template_name="addpost.html")
    elif request.method == "POST":
        title = request.POST.get("title").strip()
        description = request.POST.get("description").strip()
        image = request.FILES.get("image", None)

        if len(title or description) <= 3:
            return render(
                request=request,
                template_name="addpost.html",
                context={
                    "error": "Заголовок или Описание должен быть минимум 3 символа!"
                },
            )
        models.Post.objects.create(
            author=request.user,
            title=title,
            description=description,
            image=image,
            is_moderate=request.user.is_superuser,
        )
        return redirect(reverse("all_posts"))
    else:
        return render(
            request=request,
            template_name="addpost.html",
            context={"error": "Invalid post"},
        )


@login_required
@log_exceptions
def delete_post(request: HttpRequest, pk: str) -> HttpResponse:
    """Delete a post"""
    if request.method == "GET":
        post = get_object_or_404(Post, id=int(pk))
        post.delete()
        return redirect(reverse("all_posts"))
    else:
        return render(
            request=request,
            template_name="posts.html",
            context={"error": "Invalid post"},
        )


@login_required
@log_exceptions
def update_post(request: HttpRequest, pk: str) -> HttpResponse:
    """Update a post"""
    if request.method == "GET":
        return render(
            request=request,
            template_name="update.html",
            context={"post": models.Post.objects.get(id=int(pk))},
        )
    elif request.method == "POST":
        title = request.POST.get("title").strip()
        description = request.POST.get("description").strip()

        if len(title or description) <= 3:
            return render(
                request=request,
                template_name="update.html",
                context={
                    "error": "Заголовок или Описание должен быть минимум 3 символа!"
                },
            )
        models.Post.objects.filter(id=int(pk)).update(
            title=title,
            description=description,
            is_moderate=request.user.is_superuser,
        )
        return redirect(reverse("all_posts"))


@login_required
@log_exceptions
def detail_post(request: HttpRequest, pk: str) -> HttpResponse:
    """Post detail"""
    if request.method == "GET":
        detail = models.Post.objects.get(id=int(pk))

        post_rating_objs = models.Ratings.objects.all().filter(post=detail)

        rating = (
            post_rating_objs.filter(status=True).count()
            - post_rating_objs.filter(status=False).count()
        )

        count_r = post_rating_objs.count()

        comments = models.Comment.objects.filter(post=int(pk))

        return render(
            request=request,
            template_name="detail_view.html",
            context={
                "detail": detail,
                "comments": comments,
                "count_r": count_r,
                "rating": rating,
            },
        )
    else:
        return HttpResponse("404 Not Found", status=404)


@login_required
@log_exceptions
def comment_create(request: HttpRequest, pk: str) -> HttpResponse:
    """Create a new comment"""
    if request.method == "POST":
        author = request.user
        comment = request.POST.get("comment").strip()

        if len(comment) < 1:
            return HttpResponse("Длина коммента ниже 1! 404", status=404)

        post = models.Post.objects.get(id=int(pk))

        # Создаем комментарий и связываем его с конкретным постом
        models.Comment.objects.create(author=author, post=post, comment=comment)

        return redirect(reverse("detail_post", args=[pk]))


@login_required
@log_exceptions
def comment_delete(request: HttpRequest, pk: str) -> HttpResponse:
    """Delete a comment"""
    if request.method == "GET":
        comment = get_object_or_404(Comment, id=int(pk))
        post_pk = comment.post.pk
        comment.delete()
        return redirect(reverse("detail_post", args=[post_pk]))


@login_required
@log_exceptions
def comment_rating(request, pk: str, status) -> HttpResponse:
    """comment ratings"""

    if request.method == "GET":
        comment_obj = models.Comment.objects.get(id=int(pk))
        author_obj = request.user
        status = True if int(status) == 1 else False
        comment_rating_objs = models.CommentRatings.objects.filter(
            comment=comment_obj, author=author_obj
        )
        if len(comment_rating_objs) <= 0:
            models.CommentRatings.objects.create(
                comment=comment_obj, author=author_obj, status=status
            )
        else:
            comment_rating_obj = comment_rating_objs[0]
            if (status is True and comment_rating_obj.status is True) or (
                status is False and comment_rating_obj.status is False
            ):
                comment_rating_obj.delete()
            else:
                comment_rating_obj.status = status
                comment_rating_obj.save()

        return redirect(reverse("detail_post", args=[comment_obj.post.id]))


@login_required
@log_exceptions
def rating(request: HttpRequest, pk: str, status) -> HttpResponse:
    """post ratings"""

    if request.method == "GET":
        post_obj = models.Post.objects.get(id=int(pk))  # get the post object by id
        author_obj = request.user  # get the author
        status = True if int(status) == 1 else False
        post_rating_objs = models.Ratings.objects.filter(
            post=post_obj, author=author_obj
        )
        if len(post_rating_objs) <= 0:
            models.Ratings.objects.create(
                post=post_obj, author=author_obj, status=status
            )
        else:
            post_rating_obj = post_rating_objs[0]
            if (status is True and post_rating_obj.status is True) or (
                status is False and post_rating_obj.status is False
            ):
                post_rating_obj.delete()
            else:
                post_rating_obj.status = status
                post_rating_obj.save()
        return redirect(reverse("detail_post", args=[pk]))
    else:
        return HttpResponse("404 Not Found", status=404)


@log_exceptions
def news(request: HttpRequest) -> HttpResponse:
    news = utils.CustomPaginator.paginate(
        utils.CustomCache.caching("news", lambda_func=utils.news, timeout=60 * 30),
        request=request,
    )
    return render(
        request=request,
        template_name="news.html",
        context={"news": news},
    )


@log_exceptions
def currency(request: HttpRequest) -> HttpResponse:
    currency = utils.CustomCache.caching(
        "currency", lambda_func=utils.get_rates, timeout=1 * 5
    )

    return render(
        request=request,
        template_name="currency.html",
        context={"currency": currency},
    )
