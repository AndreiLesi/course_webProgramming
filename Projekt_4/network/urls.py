
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("post/<int:post_id>", views.post, name="post"),

    # API Routes
    path("api/posts/<int:post_id>", views.api_posts, name="api_posts"),
    path("api/follow", views.api_follow, name="api_follow"),
]
