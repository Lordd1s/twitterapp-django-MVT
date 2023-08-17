from django.urls import path
from twitter import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("add/", views.add_post, name="add_post"),
    path("allpost/", views.all_posts, name="all_posts"),
    path("delete/<str:pk>/", views.delete_post, name="delete_post"),
    path("update/<str:pk>/", views.update_post, name="update_post"),
    path("detail/<str:pk>/", views.detail_post, name="detail_post"),
    path("comments/<str:pk>/", views.comment_create, name="comment_create"),
    path("comment_delete/<str:pk>/", views.comment_delete, name="comment_delete"),
    path("rating/<str:pk>/<str:status>/", views.rating, name="rating"),
    path("news/", views.news, name="news"),
    path("comments_rating/<str:pk>/<str:status>/", views.comment_rating, name="comment_rating"),
    path("currency", views.currency, name="currency"),
]
