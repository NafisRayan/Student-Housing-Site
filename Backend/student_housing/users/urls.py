from django.urls import path

from . import views

urlpatterns = [
    path("", views.users_intro, name="users_intro"),
    path("login/", views.users_login, name="users_login"),
    path("register/", views.users_register, name="users_register"),
    path("profile/<str:username>/", views.users_profile, name="users_profile"),
    path("create-post/", views.create_post, name="create_post"),
    path("logout/", views.users_logout, name="users_logout"),
]