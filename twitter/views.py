import random

import bcrypt  # password hashing library
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from twitter import models
from twitter.models import Post, Comment

from twitter import utils


# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    """Return to home page"""
    return render(request=request, template_name="home.html")


def register(request: HttpRequest) -> HttpResponse:
    """Register a new user."""
    if request.method == "GET":
        return render(request=request, template_name="login-registration.html")

    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
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
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        new_user = User.objects.create_user(
            username=username, password=hashed_password, email=email
        )

        # Log in the newly registered user
        login(request, user=new_user)
        print("successfully created new user")
        return redirect(reverse("home"))


def login_user(request: HttpRequest) -> HttpResponse:
    """Login a user."""
    if request.method == "GET":
        return render(request=request, template_name="login-registration.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not (username and password):
            return render(
                request=request,
                template_name="login-registration.html",
                context={"error": "Invalid credentials."},
            )

        user = authenticate(
            username=username,
            password=password,
            # password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()),
        )

        if user is not None:
            # User is valid, and login is successful.
            login(request, user=user)
            return redirect(reverse("home"))
        else:
            # Invalid login credentials.
            return render(
                request=request,
                template_name="login-registration.html",
                context={"error": "Invalid credentials."},
            )


def logout_user(request: HttpRequest) -> redirect:
    """Logout a user."""
    logout(request)

    return redirect(reverse("home"))


def all_posts(request: HttpRequest) -> HttpResponse:
    """Returns all the posts"""
    posts = models.Post.objects.all().filter(is_moderate=True).order_by("-date_created")

    if request.method == "GET":
        return render(
            request=request,
            template_name="posts.html",
            context={
                "posts": posts,
                "test_beautify_tag": random.randint(1000000, 9999999),
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


def add_post(request: HttpRequest) -> HttpResponse:
    """Add a post"""
    if request.method == "GET":
        return render(request=request, template_name="addpost.html")
    elif request.method == "POST":
        title = request.POST.get("title").strip()
        description = request.POST.get("description").strip()
        image = request.FILES.get("image", None)
        print(image)

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


def comment_delete(request: HttpRequest, pk: str) -> HttpResponse:
    """Delete a comment"""
    if request.method == "GET":
        comment = get_object_or_404(Comment, id=int(pk))
        post_pk = comment.post.pk
        comment.delete()
        return redirect(reverse("detail_post", args=[post_pk]))


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


def news(request: HttpRequest) -> HttpResponse:
    return render(
        request=request, template_name="news.html", context={"news": utils.news()}
    )


def currency(request: HttpRequest) -> HttpResponse:
    return render(
        request=request,
        template_name="currency.html",
        context={"currency": utils.get_rates()},
    )
