from django.urls import path
from twitter import views


urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/login/", views.login_user, name="login"),
    path("profile/", views.profile, name="profile"),
    path("delete_profile", views.delete_profile, name="delete_profile"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("send_message/", views.message, name="message"),
    path("all_messages/", views.all_messages, name="all_messages"),
    path(
        "detail_message/<str:subject>/<str:sender_id>/<str:recipient_id>",
        views.detail_message,
        name="detail_message",
    ),
    path(
        "delete_message/<str:subject>/<str:sender_id>/<str:recipient_id>",
        views.delete_message,
        name="delete_message",
    ),
    path(
        "edit_message/<str:subject>/<str:sender_id>/<str:recipient_id>",
        views.edit_message,
        name="edit_message",
    ),
    path("add/", views.add_post, name="add_post"),
    path("allpost/", views.all_posts, name="all_posts"),
    path("delete/<str:pk>/", views.delete_post, name="delete_post"),
    path("update/<str:pk>/", views.update_post, name="update_post"),
    path("detail/<str:pk>/", views.detail_post, name="detail_post"),
    path("comments/<str:pk>/", views.comment_create, name="comment_create"),
    path("comment_delete/<str:pk>/", views.comment_delete, name="comment_delete"),
    path("rating/<str:pk>/<str:status>/", views.rating, name="rating"),
    path("news/", views.news, name="news"),
    path(
        "comments_rating/<str:pk>/<str:status>/",
        views.comment_rating,
        name="comment_rating",
    ),
    path("currency", views.currency, name="currency"),
]
